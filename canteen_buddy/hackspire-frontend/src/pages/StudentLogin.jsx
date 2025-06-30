import { useOutletContext } from "react-router-dom"

function StudentLoginPage() {
    const {developmentBackendLink, productionBackendLink, login, setLogin, adminLogin, setAdminLogin, setAlert} = useOutletContext();
    
    const handleLogin = (event) => {
        event.preventDefault()

        let username = event.target.username.value
        let password = event.target.password.value

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password,
            })
        }

        fetch(`${developmentBackendLink}/student-login`)
            .then((response) => response.json())
            .then((data) => {
                if (data.error_message) {
                    setAlert(data.error_message)
                    return
                }
                sessionStorage.setItem("")
            })
    }

    return (
        <div>
            <br />
            <form method="post" style={{width: "50%", marginLeft: "auto", marginRight: "auto", textAlign: "start"}} onSubmit={handleLogin}>
                <h1 style={{"textAlign": "center"}}>Login</h1>

                <label htmlFor="username" className="form-label">Username:</label>
                <input type="text" name="username" id="username" placeholder="Enter student's name" className="form-control" />
                <br />
                <label htmlFor="password" className="form-label">Password:</label>
                <input type="text" name="password" id="password" placeholder="Enter student's password" className="form-control" />
                <br />
                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    )
}

export default StudentLoginPage