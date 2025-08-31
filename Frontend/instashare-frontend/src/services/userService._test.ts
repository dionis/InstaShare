import { userService, User, UserListResponse, DeleteResponse, UserDocumentsResponse } from './userService';
import api from './api'; // Mocked by Jest

jest.mock('./api');
const mockedApi = api as jest.Mocked<typeof api>;

describe('userService', () => {
  beforeEach(() => {
    mockedApi.get.mockClear();
    mockedApi.post.mockClear();
    mockedApi.put.mockClear();
    mockedApi.delete.mockClear();
  });

  test('getUsers should fetch a list of users', async () => {
    const mockUsers: UserListResponse = [
      { id: 1, name: 'John Doe', email: 'john@example.com', phone: '+123', responsability: 'Dev', role: 'user' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com', phone: '+456', responsability: 'QA', role: 'admin' },
    ];
    mockedApi.get.mockResolvedValueOnce({ data: mockUsers });

    const users = await userService.getUsers();

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/users/');
    expect(users).toEqual(mockUsers);
  });

  test('getUserById should fetch a single user by ID', async () => {
    const mockUser: User = { id: 1, name: 'John Doe', email: 'john@example.com', phone: '+123', responsability: 'Dev', role: 'user' };
    mockedApi.get.mockResolvedValueOnce({ data: mockUser });

    const user = await userService.getUserById(1);

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/users/1');
    expect(user).toEqual(mockUser);
  });

  test('createUser should create a new user', async () => {
    const newUser: Omit<User, 'id' | 'role' | 'created_at' | 'updated_at' | 'deleted_at'> = {
      name: 'New User', email: 'new@example.com', phone: '+789', responsability: 'Designer', password: ''
    };
    const createdUser: User = { ...newUser, id: 3, role: 'user' };
    mockedApi.post.mockResolvedValueOnce({ data: createdUser });

    const user = await userService.createUser(newUser);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/users/', newUser);
    expect(user).toEqual(createdUser);
  });

  test('updateUser should update an existing user', async () => {
    const updatedUserData: Partial<Omit<User, 'id' | 'role' | 'created_at' | 'updated_at' | 'deleted_at'>> = { name: 'Updated Name' };
    const updatedUser: User = { id: 1, name: 'Updated Name', email: 'john@example.com', phone: '+123', responsability: 'Dev', role: 'user' };
    mockedApi.put.mockResolvedValueOnce({ data: updatedUser });

    const user = await userService.updateUser(1, updatedUserData);

    expect(mockedApi.put).toHaveBeenCalledTimes(1);
    expect(mockedApi.put).toHaveBeenCalledWith('/updated_user/1', updatedUserData);
    expect(user).toEqual(updatedUser);
  });

  test('deleteUser should delete a user by ID', async () => {
    const deleteResponse: DeleteResponse = { action: 'deleted', message: 'Document deleted' }; // Using Document deleted as per contract
    mockedApi.delete.mockResolvedValueOnce({ data: deleteResponse });

    const response = await userService.deleteUser(1);

    expect(mockedApi.delete).toHaveBeenCalledTimes(1);
    expect(mockedApi.delete).toHaveBeenCalledWith('/users/1');
    expect(response).toEqual(deleteResponse);
  });

  test('getDocumentsUploadedByUser should fetch documents for a user', async () => {
    const mockUserDocuments: UserDocumentsResponse = {
      id: 1, name: 'John Doe', email: 'john@example.com', phone: '+123', responsability: 'Dev', role: 'user',
      upload_documents: [
        { id: 101, name: 'doc1', type: 'pdf', size: '1MB', uploaded_at: '2024-01-01' },
      ],
    };
    mockedApi.get.mockResolvedValueOnce({ data: mockUserDocuments });

    const userDocs = await userService.getDocumentsUploadedByUser(1);

    expect(mockedApi.get).toHaveBeenCalledTimes(1);
    expect(mockedApi.get).toHaveBeenCalledWith('/documents_upload_by_user/1');
    expect(userDocs).toEqual(mockUserDocuments);
  });

  test('assignRoleToUser should assign a role to a user', async () => {
    const mockResponse = { status: 'success' };
    mockedApi.post.mockResolvedValueOnce({ data: mockResponse });

    const response = await userService.assignRoleToUser(1, 10);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/add_role/10/user/1');
    expect(response).toEqual(mockResponse);
  });

  test('createRoleEvent should create a role event', async () => {
    const eventData = { event: 'role_assigned', user_id: 1, event_description: 'Role assigned to user 1' };
    const mockResponse = { idjob: 1, event: 'role_assigned' };
    mockedApi.post.mockResolvedValueOnce({ data: mockResponse });

    const response = await userService.createRoleEvent(eventData);

    expect(mockedApi.post).toHaveBeenCalledTimes(1);
    expect(mockedApi.post).toHaveBeenCalledWith('/create_role_evet/', eventData);
    expect(response).toEqual(mockResponse);
  });
});






