"use client"

import { useState, useEffect } from "react"
import { FiEdit2, FiTrash2, FiCheckCircle, FiXCircle, FiSearch } from "react-icons/fi"
import { toast } from "react-toastify"
import "./AdminUsers.css"

const AdminUsers = () => {
  const [users, setUsers] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState("")
  const [editingUser, setEditingUser] = useState(null)

  useEffect(() => {
    fetchUsers()
  }, [])

  const fetchUsers = async () => {
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch("/api/admin/users", {
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        setUsers(data.users)
      } else {
        toast.error("Failed to load users")
      }
    } catch (error) {
      console.error("Error fetching users:", error)
      toast.error("Failed to load users")
    } finally {
      setLoading(false)
    }
  }

  const deleteUser = async (userId) => {
    if (!window.confirm("Are you sure you want to delete this user?")) return

    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch(`/api/admin/users/${userId}`, {
        method: "DELETE",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        toast.success("User deleted successfully")
        fetchUsers()
      } else {
        toast.error(data.error || "Failed to delete user")
      }
    } catch (error) {
      console.error("Error deleting user:", error)
      toast.error("Failed to delete user")
    }
  }

  const verifyUser = async (userId) => {
    try {
      const token = localStorage.getItem("jwt_token")
      const response = await fetch(`/api/admin/users/${userId}/verify`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${token}`,
        },
      })

      const data = await response.json()
      if (data.success) {
        toast.success("User verified successfully")
        fetchUsers()
      } else {
        toast.error(data.error || "Failed to verify user")
      }
    } catch (error) {
      console.error("Error verifying user:", error)
      toast.error("Failed to verify user")
    }
  }

  const filteredUsers = users.filter(
    (user) =>
      user.name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.email?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      user.username?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  if (loading) {
    return (
      <div className="admin-page">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading users...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="admin-page">
      <div className="page-header">
        <h1>User Management</h1>
        <p>Manage all users in the system</p>
      </div>

      <div className="search-bar">
        <FiSearch className="search-icon" />
        <input
          type="text"
          placeholder="Search users by name, email, or username..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
      </div>

      <div className="users-table-container">
        <table className="users-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Email</th>
              <th>Username</th>
              <th>Role</th>
              <th>Verified</th>
              <th>Created</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredUsers.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.name}</td>
                <td>{user.email}</td>
                <td>{user.username || "-"}</td>
                <td>
                  <span className={`role-badge ${user.role}`}>{user.role}</span>
                </td>
                <td>
                  {user.is_verified ? (
                    <FiCheckCircle className="icon-verified" />
                  ) : (
                    <FiXCircle className="icon-unverified" />
                  )}
                </td>
                <td>{new Date(user.created_at).toLocaleDateString()}</td>
                <td className="actions">
                  {!user.is_verified && (
                    <button
                      className="btn-verify"
                      onClick={() => verifyUser(user.id)}
                      title="Verify User"
                    >
                      <FiCheckCircle />
                    </button>
                  )}
                  <button
                    className="btn-delete"
                    onClick={() => deleteUser(user.id)}
                    title="Delete User"
                  >
                    <FiTrash2 />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {filteredUsers.length === 0 && (
          <div className="no-results">
            <p>No users found matching your search.</p>
          </div>
        )}
      </div>

      <div className="users-summary">
        <p>
          Showing <strong>{filteredUsers.length}</strong> of <strong>{users.length}</strong> users
        </p>
      </div>
    </div>
  )
}

export default AdminUsers


