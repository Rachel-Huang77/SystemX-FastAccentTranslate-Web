// src/api/admin.js
const BASE_URL = import.meta.env.VITE_API_BASE_URL + "/api/v1/admin";

async function api(path, { method = "GET", body, params } = {}) {
  // 构建 URL
  let url = `${BASE_URL}${path}`;

  // 添加查询参数
  if (params) {
    const query = new URLSearchParams(params).toString();
    url += `?${query}`;
  }

  const res = await fetch(url, {
    method,
    headers: body ? { "Content-Type": "application/json" } : undefined,
    body: body ? JSON.stringify(body) : undefined,
    credentials: "include", // 带上 HttpOnly Cookie
  });

  let data = null;
  try {
    data = await res.json();
  } catch (_) {}

  if (!res.ok || (data && data.success === false)) {
    let msg;

    // 处理 FastAPI 的验证错误（detail 是数组）
    if (Array.isArray(data?.detail)) {
      msg = data.detail.map(err => err.msg || JSON.stringify(err)).join("; ");
    } else {
      msg = data?.error?.message || data?.detail || `HTTP ${res.status}`;
    }

    return { ok: false, message: msg, code: data?.error?.code };
  }

  return { ok: true, data: data?.data ?? data };
}

/**
 * 获取用户列表
 */
export async function getUserList(params = {}) {
  const defaultParams = {
    page: 1,
    limit: 20,
    ...params
  };
  return await api("/users", { method: "GET", params: defaultParams });
}

/**
 * 获取用户详情
 */
export async function getUserDetail(userId) {
  return await api(`/users/${userId}`, { method: "GET" });
}

/**
 * 创建用户
 */
export async function createUser(userData) {
  return await api("/users", { method: "POST", body: userData });
}

/**
 * 更新用户信息
 */
export async function updateUser(userId, updates) {
  return await api(`/users/${userId}`, { method: "PUT", body: updates });
}

/**
 * 重置用户密码
 */
export async function resetUserPassword(userId, newPassword) {
  return await api(`/users/${userId}/reset-password`, {
    method: "POST",
    body: { new_password: newPassword }
  });
}

/**
 * 删除用户
 */
export async function deleteUser(userId, cascade = true) {
  return await api(`/users/${userId}`, {
    method: "DELETE",
    params: { cascade }
  });
}

/**
 * 批量删除用户
 */
export async function batchDeleteUsers(userIds, cascade = true) {
  return await api("/users/batch-delete", {
    method: "POST",
    body: { user_ids: userIds, cascade }
  });
}
