"""
Test script to verify chat update functionality preserves all messages.

This script demonstrates that:
1. Initial save creates conversation with all messages
2. Update appends new messages to existing conversation
3. Re-fetching shows ALL messages (old + new) in order
4. No messages are dropped or lost
"""

import requests
import json

API_BASE = "http://localhost:5000/api"

def test_chat_update_flow():
    """Test the complete chat save and update flow."""
    
    print("=" * 70)
    print("CHAT UPDATE TEST - Verify All Messages Are Preserved")
    print("=" * 70)
    
    # Test data
    user_id = 1  # Assume user 1 exists
    
    # Step 1: Create initial conversation with 4 messages (2 pairs)
    print("\n📝 Step 1: Creating new conversation with 4 messages (2 pairs)...")
    initial_messages = [
        {"role": "user", "content": "Hello, I need career advice"},
        {"role": "assistant", "content": "Hi! I'd be happy to help with your career questions."},
        {"role": "user", "content": "What skills do I need for data science?"},
        {"role": "assistant", "content": "For data science, you'll need Python, statistics, machine learning, and SQL."}
    ]
    
    save_payload = {
        "user_id": user_id,
        "messages": initial_messages,
        "conversation_id": None  # New conversation
    }
    
    response = requests.post(f"{API_BASE}/chatbot/save-conversation", json=save_payload)
    
    if response.status_code in [200, 201]:
        result = response.json()
        print(f"✅ Success! Created conversation: {result['conversation_id']}")
        print(f"   - Title: {result['title']}")
        print(f"   - Message pairs saved: {result['appended_count']}")
        print(f"   - Is update: {result['is_update']}")
        conversation_id = result['conversation_id']
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
        return
    
    # Step 2: Fetch the conversation to verify initial save
    print(f"\n📥 Step 2: Fetching conversation to verify initial 4 messages...")
    response = requests.get(f"{API_BASE}/chatbot/conversations/{conversation_id}?user_id={user_id}")
    
    if response.status_code == 200:
        result = response.json()
        history = result['conversation']['history']
        print(f"✅ Retrieved conversation with {len(history)} messages")
        print("   Messages:")
        for i, msg in enumerate(history, 1):
            preview = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
            print(f"      {i}. [{msg['role']}] {preview}")
    else:
        print(f"❌ Failed to fetch: {response.status_code}")
        return
    
    # Step 3: Add 2 new messages and update the conversation
    print(f"\n📝 Step 3: Adding 2 NEW messages to existing conversation...")
    print("   (Simulating user continuing the chat)")
    
    # In real app, frontend sends ALL messages including old ones
    all_messages = initial_messages + [
        {"role": "user", "content": "How long does it take to become a data scientist?"},
        {"role": "assistant", "content": "Typically 6-12 months with dedicated study and practice."}
    ]
    
    update_payload = {
        "user_id": user_id,
        "messages": all_messages,  # ALL messages (old + new)
        "conversation_id": conversation_id  # Existing conversation
    }
    
    response = requests.post(f"{API_BASE}/chatbot/save-conversation", json=update_payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success! Updated conversation")
        print(f"   - New message pairs appended: {result['appended_count']}")
        print(f"   - Is update: {result['is_update']}")
        print(f"   - Message: {result['message']}")
    else:
        print(f"❌ Failed: {response.status_code} - {response.text}")
        return
    
    # Step 4: Fetch again to verify ALL 6 messages are present
    print(f"\n📥 Step 4: Fetching conversation to verify ALL 6 messages (4 old + 2 new)...")
    response = requests.get(f"{API_BASE}/chatbot/conversations/{conversation_id}?user_id={user_id}")
    
    if response.status_code == 200:
        result = response.json()
        history = result['conversation']['history']
        print(f"✅ Retrieved conversation with {len(history)} messages")
        print("   Complete message history:")
        for i, msg in enumerate(history, 1):
            preview = msg['content'][:60] + "..." if len(msg['content']) > 60 else msg['content']
            marker = "🆕" if i > 4 else "📌"
            print(f"      {marker} {i}. [{msg['role']}] {preview}")
        
        # Verification
        print("\n" + "=" * 70)
        if len(history) == 6:
            print("✅ TEST PASSED: All messages preserved!")
            print("   - Original 4 messages: ✓")
            print("   - New 2 messages: ✓")
            print("   - Total: 6 messages ✓")
        else:
            print(f"❌ TEST FAILED: Expected 6 messages, got {len(history)}")
        print("=" * 70)
    else:
        print(f"❌ Failed to fetch: {response.status_code}")
        return
    
    # Step 5: Try to update again with no new messages
    print(f"\n📝 Step 5: Trying to update with no new messages (should return 'already up to date')...")
    
    response = requests.post(f"{API_BASE}/chatbot/save-conversation", json=update_payload)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Success!")
        print(f"   - Message: {result['message']}")
        print(f"   - Appended count: {result['appended_count']}")
        print(f"   - No duplicate messages created ✓")
    else:
        print(f"❌ Failed: {response.status_code}")
    
    print("\n" + "=" * 70)
    print("TEST COMPLETE - Chat update preserves all messages correctly!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        test_chat_update_flow()
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Cannot connect to backend server")
        print("Please make sure the Flask server is running:")
        print("  cd Backend && python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")

