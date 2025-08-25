import api from './api';

export interface User {
  id: number;
  name: string;
  email: string;
  phone: string;
  responsability: string;
  role: string;
  password?: string; // Only for creation/update, not typically returned
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
}

export interface UserListResponse extends Array<User> {}

export interface UserDocumentsResponse extends User {
  upload_documents: Document[];
}

export interface DeleteResponse {
  action: string;
  message: string;
}

// Assuming Document interface is defined elsewhere or will be defined in documentService.ts
interface Document {
  id: number;
  name: string;
  type: string;
  size: string;
  uploaded_at: string;
  created_at?: string;
  updated_at?: string;
  deleted_at?: string;
  status?: "uploaded" | "process" | "downloaded";
}

export const userService = {
  getUsers: async (): Promise<UserListResponse> => {
    const response = await api.get<UserListResponse>('/users/');
    return response.data;
  },

  getUserById: async (id: number): Promise<User> => {
    const response = await api.get<User>(`/users/${id}`);
    return response.data;
  },

  createUser: async (userData: Omit<User, 'id' | 'role' | 'created_at' | 'updated_at' | 'deleted_at'>): Promise<User> => {
    const response = await api.post<User>('/create_user/', userData);
    return response.data;
  },

  updateUser: async (id: number, userData: Partial<Omit<User, 'id' | 'role' | 'created_at' | 'updated_at' | 'deleted_at'>>): Promise<User> => {
    const response = await api.put<User>(`/updated_user/${id}`, userData);
    return response.data;
  },

  deleteUser: async (id: number): Promise<DeleteResponse> => {
    const response = await api.delete<DeleteResponse>(`/delete_user/${id}`);
    return response.data;
  },

  getDocumentsUploadedByUser: async (id: number): Promise<UserDocumentsResponse> => {
    const response = await api.get<UserDocumentsResponse>(`/documents_upload_by_user/${id}`);
    return response.data;
  },

  assignRoleToUser: async (userId: number, roleId: number): Promise<any> => { // Adjust return type as per backend contract
    const response = await api.post(`/add_role/${roleId}/user/${userId}`);
    return response.data;
  },

  createRoleEvent: async (eventData: any): Promise<any> => { // Adjust return type as per backend contract
    const response = await api.post('/create_role_evet/', eventData);
    return response.data;
  },
};



