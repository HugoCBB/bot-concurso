import axios from "axios";

const api = axios.create({
    baseURL: "http://127.0.0.1:8000",
    withCredentials: true,
    headers: {
        "Content-Type": "application/json",
    }
})

export const contestsApi = {
    get_contests: async (page: number = 1, size: number = 50) => {
        const response = await api.get(`/api/contests/?page=${page}&size=${size}`)
        return response.data
    }
}