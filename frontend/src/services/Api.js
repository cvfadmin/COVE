import axios from 'axios'
import store from '@/store'
import router from '@/router'

export default () => {
    const instance = axios.create({
        baseURL: `http://localhost:5000/`,
        withCredentials: true,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json', 
            'crossdomain': true,
            'Authorization': 'Bearer ' + store.state.accessToken
        }
    })

    // Response interceptor for error 401 (token expires)
    // Put functions in separate files
    instance.interceptors.response.use(function (response) {
        return response;
    }, function (error) {
        // Redirects user to login page.
        if (error.response.status == 401) {
            alert("Session expired. Please log in again.")
            store.dispatch('logout')
            router.push({ name: 'login' })
        }
        return Promise.reject(error);
    });

    return instance
}