const axios = require('axios');

export const saveRedis = async (id, value) => {
    let status = false
    let url = (process.env.REACT_APP_BACKEND1_URL !== undefined) ? process.env.REACT_APP_BACKEND1_URL : 'http://localhost:8080'

    await axios.get(url)
        .then((response) => {
            if (response.status === 200) {
                status = true
            }
        })
        .catch((err) => {
            console.error(err)
        })

    return status
}
