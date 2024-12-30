export async function login() {
    let response = await fetch('api/token/')
    if (response.ok) {
        let json = await response.json();
        sessionStorage.setItem('token', json['token'])
        sessionStorage.setItem('user_name', json['user_name'])
        return true
    }

    return false
}

export async function get_users() {
    return await fetch('api/users/', {
        headers: {
            Authentication: 'Token ' + sessionStorage.getItem('token')
        }
    })
}

export async function get_chats() {
    return await fetch('api/chats/', {
        headers: {
            Authentication: 'Token ' + sessionStorage.getItem('token')
        }
    })
}

export async function upload_file(formData: FormData) {
    return await fetch('api/uploadfile/', {
        method: 'POST',
        headers: {
            'Content-Type': 'multipart/form-data'
        },
        body: JSON.stringify(formData),
    })
}