import axios from 'axios'
import store from '@/store'

export default () => {
    return axios.create({
        baseURL: `http://localhost:5000/`,
        withCredentials: true,
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json', 
            'crossdomain': true,
            'Authorization': 'Bearer ' + store.state.accessToken
        }
    })
}