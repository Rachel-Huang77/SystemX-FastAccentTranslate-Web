import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./UserManagement.module.css";
import {
  getUserList,
  createUser,
  updateUser,
  deleteUser,
  resetUserPassword,
  batchDeleteUsers
} from "../../api/admin";

export default function UserManagement() {
  const navigate = useNavigate();

  // User list state
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [page, setPage] = useState(1);
  const [limit] = useState(20);
  const [total, setTotal] = useState(0);
  const [searchTerm, setSearchTerm] = useState("");
  const [roleFilter, setRoleFilter] = useState("");
  const [statusFilter, setStatusFilter] = useState("");

  // Selected users for batch operations
  const [selectedUsers, setSelectedUsers] = useState([]);

  // Modal states
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [showEditModal, setShowEditModal] = useState(false);
  const [showResetPasswordModal, setShowResetPasswordModal] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);

  // Form states
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
    role: "user"
  });
  const [newPassword, setNewPassword] = useState("");

  // Current logged-in user
  const currentUserId = localStorage.getItem("authUserId");

  // Load users on mount and when filters change
  useEffect(() => {
    loadUsers();
  }, [page, searchTerm, roleFilter, statusFilter]);

  const loadUsers = async () => {
    setLoading(true);
    try {
      const params = {
        page,
        limit
      };

      // 只添加有值的参数
      if (searchTerm) params.search = searchTerm;
      if (roleFilter) params.role = roleFilter;
      if (statusFilter === "active") params.is_active = true;
      if (statusFilter === "inactive") params.is_active = false;

      const resp = await getUserList(params);
      if (resp.ok) {
        setUsers(resp.data.users || []);
        setTotal(resp.data.pagination?.total || 0);
      } else {
        alert(resp.message || "Failed to load users");
      }
    } catch (err) {
      alert(err.message || "Error loading users");
    } finally {
      setLoading(false);
    }
  };

  const handleCreateUser = async (e) => {
    e.preventDefault();
    if (!formData.username || !formData.email || !formData.password) {
      alert("Please fill in all required fields");
      return;
    }

    setLoading(true);
    try {
      const resp = await createUser(formData);
      if (resp.ok) {
        alert("User created successfully");
        setShowCreateModal(false);
        resetForm();
        loadUsers();
      } else {
        alert(resp.message || "Failed to create user");
      }
    } catch (err) {
      alert(err.message || "Error creating user");
    } finally {
      setLoading(false);
    }
  };

  const handleUpdateUser = async (e) => {
    e.preventDefault();
    if (!currentUser) return;

    setLoading(true);
    try {
      const updates = {
        username: formData.username,
        email: formData.email,
        role: formData.role
      };

      const resp = await updateUser(currentUser.id, updates);
      if (resp.ok) {
        alert("User updated successfully");
        setShowEditModal(false);
        resetForm();
        loadUsers();
      } else {
        alert(resp.message || "Failed to update user");
      }
    } catch (err) {
      alert(err.message || "Error updating user");
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    if (!currentUser || !newPassword) {
      alert("Please enter a new password");
      return;
    }

    setLoading(true);
    try {
      const resp = await resetUserPassword(currentUser.id, newPassword);
      if (resp.ok) {
        alert("Password reset successfully");
        setShowResetPasswordModal(false);
        setNewPassword("");
        setCurrentUser(null);
      } else {
        alert(resp.message || "Failed to reset password");
      }
    } catch (err) {
      alert(err.message || "Error resetting password");
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteUser = async (user) => {
    if (user.id === currentUserId) {
      alert("You cannot delete yourself!");
      return;
    }

    if (!confirm(`Are you sure you want to delete user "${user.username}"?`)) {
      return;
    }

    setLoading(true);
    try {
      const resp = await deleteUser(user.id);
      if (resp.ok) {
        alert("User deleted successfully");
        loadUsers();
      } else {
        alert(resp.message || "Failed to delete user");
      }
    } catch (err) {
      alert(err.message || "Error deleting user");
    } finally {
      setLoading(false);
    }
  };

  const handleBatchDelete = async () => {
    if (selectedUsers.length === 0) {
      alert("Please select users to delete");
      return;
    }

    if (selectedUsers.includes(currentUserId)) {
      alert("You cannot delete yourself!");
      return;
    }

    if (!confirm(`Are you sure you want to delete ${selectedUsers.length} user(s)?`)) {
      return;
    }

    setLoading(true);
    try {
      const resp = await batchDeleteUsers(selectedUsers);
      if (resp.ok) {
        alert(`Successfully deleted ${selectedUsers.length} user(s)`);
        setSelectedUsers([]);
        loadUsers();
      } else {
        alert(resp.message || "Failed to delete users");
      }
    } catch (err) {
      alert(err.message || "Error deleting users");
    } finally {
      setLoading(false);
    }
  };

  const openEditModal = (user) => {
    setCurrentUser(user);
    setFormData({
      username: user.username,
      email: user.email,
      password: "",
      role: user.role
    });
    setShowEditModal(true);
  };

  const openResetPasswordModal = (user) => {
    setCurrentUser(user);
    setNewPassword("");
    setShowResetPasswordModal(true);
  };

  const resetForm = () => {
    setFormData({
      username: "",
      email: "",
      password: "",
      role: "user"
    });
    setCurrentUser(null);
  };

  const toggleUserSelection = (userId) => {
    setSelectedUsers(prev =>
      prev.includes(userId)
        ? prev.filter(id => id !== userId)
        : [...prev, userId]
    );
  };

  const toggleSelectAll = () => {
    if (selectedUsers.length === users.length) {
      setSelectedUsers([]);
    } else {
      setSelectedUsers(users.map(u => u.id));
    }
  };

  const totalPages = Math.ceil(total / limit);

  return (
    <div className={styles.container}>
      <div className={styles.header}>
        <h1>User Management</h1>
        <button
          className={styles.backBtn}
          onClick={() => navigate("/dashboard")}
        >
          ← Back to Dashboard
        </button>
      </div>

      {/* Filters and Actions */}
      <div className={styles.toolbar}>
        <div className={styles.filters}>
          <input
            type="text"
            placeholder="Search by username or email..."
            value={searchTerm}
            onChange={(e) => {
              setSearchTerm(e.target.value);
              setPage(1);
            }}
            className={styles.searchInput}
          />

          <select
            value={roleFilter}
            onChange={(e) => {
              setRoleFilter(e.target.value);
              setPage(1);
            }}
            className={styles.filterSelect}
          >
            <option value="">All Roles</option>
            <option value="user">User</option>
            <option value="admin">Admin</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => {
              setStatusFilter(e.target.value);
              setPage(1);
            }}
            className={styles.filterSelect}
          >
            <option value="">All Status</option>
            <option value="active">Active</option>
            <option value="inactive">Inactive</option>
          </select>
        </div>

        <div className={styles.actions}>
          <button
            className={styles.createBtn}
            onClick={() => setShowCreateModal(true)}
          >
            + Create User
          </button>

          {selectedUsers.length > 0 && (
            <button
              className={styles.deleteBtn}
              onClick={handleBatchDelete}
            >
              Delete Selected ({selectedUsers.length})
            </button>
          )}
        </div>
      </div>

      {/* User Table */}
      <div className={styles.tableContainer}>
        {loading && <div className={styles.loader}>Loading...</div>}

        {!loading && users.length === 0 && (
          <div className={styles.empty}>No users found</div>
        )}

        {!loading && users.length > 0 && (
          <table className={styles.table}>
            <thead>
              <tr>
                <th>
                  <input
                    type="checkbox"
                    checked={selectedUsers.length === users.length}
                    onChange={toggleSelectAll}
                  />
                </th>
                <th>Username</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Created At</th>
                <th>Last Login</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {users.map(user => (
                <tr key={user.id}>
                  <td>
                    <input
                      type="checkbox"
                      checked={selectedUsers.includes(user.id)}
                      onChange={() => toggleUserSelection(user.id)}
                      disabled={user.id === currentUserId}
                    />
                  </td>
                  <td>{user.username}</td>
                  <td>{user.email}</td>
                  <td>
                    <span className={`${styles.badge} ${styles[user.role]}`}>
                      {user.role}
                    </span>
                  </td>
                  <td>
                    <span className={`${styles.badge} ${user.is_active ? styles.active : styles.inactive}`}>
                      {user.is_active ? "Active" : "Inactive"}
                    </span>
                  </td>
                  <td>{new Date(user.created_at).toLocaleDateString()}</td>
                  <td>{user.last_login ? new Date(user.last_login).toLocaleDateString() : "Never"}</td>
                  <td>
                    <div className={styles.actionBtns}>
                      <button
                        className={styles.actionBtn}
                        onClick={() => openEditModal(user)}
                        title="Edit user"
                      >
                        ✏️
                      </button>
                      <button
                        className={styles.actionBtn}
                        onClick={() => openResetPasswordModal(user)}
                        title="Reset password"
                      >
                        🔑
                      </button>
                      <button
                        className={styles.actionBtn}
                        onClick={() => handleDeleteUser(user)}
                        disabled={user.id === currentUserId}
                        title="Delete user"
                      >
                        🗑️
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className={styles.pagination}>
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1}
          >
            Previous
          </button>
          <span>Page {page} of {totalPages}</span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages}
          >
            Next
          </button>
        </div>
      )}

      {/* Create User Modal */}
      {showCreateModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2>Create New User</h2>
            <form onSubmit={handleCreateUser}>
              <label>
                Username *
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  required
                />
              </label>

              <label>
                Email *
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </label>

              <label>
                Password *
                <input
                  type="password"
                  value={formData.password}
                  onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                  required
                  minLength={8}
                />
                <small>Minimum 8 characters, must include uppercase, lowercase, and number</small>
              </label>

              <label>
                Role
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </label>

              <div className={styles.modalActions}>
                <button type="submit" className={styles.primaryBtn} disabled={loading}>
                  {loading ? "Creating..." : "Create"}
                </button>
                <button
                  type="button"
                  className={styles.secondaryBtn}
                  onClick={() => {
                    setShowCreateModal(false);
                    resetForm();
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Edit User Modal */}
      {showEditModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2>Edit User</h2>
            <form onSubmit={handleUpdateUser}>
              <label>
                Username *
                <input
                  type="text"
                  value={formData.username}
                  onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                  required
                />
              </label>

              <label>
                Email *
                <input
                  type="email"
                  value={formData.email}
                  onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                  required
                />
              </label>

              <label>
                Role
                <select
                  value={formData.role}
                  onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </label>

              <div className={styles.modalActions}>
                <button type="submit" className={styles.primaryBtn} disabled={loading}>
                  {loading ? "Updating..." : "Update"}
                </button>
                <button
                  type="button"
                  className={styles.secondaryBtn}
                  onClick={() => {
                    setShowEditModal(false);
                    resetForm();
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Reset Password Modal */}
      {showResetPasswordModal && (
        <div className={styles.modal}>
          <div className={styles.modalContent}>
            <h2>Reset Password for {currentUser?.username}</h2>
            <form onSubmit={handleResetPassword}>
              <label>
                New Password *
                <input
                  type="password"
                  value={newPassword}
                  onChange={(e) => setNewPassword(e.target.value)}
                  required
                  minLength={8}
                />
                <small>Minimum 8 characters, must include uppercase, lowercase, and number</small>
              </label>

              <div className={styles.modalActions}>
                <button type="submit" className={styles.primaryBtn} disabled={loading}>
                  {loading ? "Resetting..." : "Reset Password"}
                </button>
                <button
                  type="button"
                  className={styles.secondaryBtn}
                  onClick={() => {
                    setShowResetPasswordModal(false);
                    setNewPassword("");
                    setCurrentUser(null);
                  }}
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
