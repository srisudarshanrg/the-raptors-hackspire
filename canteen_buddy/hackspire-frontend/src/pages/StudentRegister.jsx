import { useOutletContext } from "react-router-dom";

function StudentRegisterPage() {
    const {developmentBackendLink, productionBackendLink, login, setLogin, adminLogin, setAdminLogin, setAlert} = useOutletContext();

    const registerSubmit = (event) => {
        event.preventDefault()

        let username = event.target.username.value
        let section = event.target.section.value
        let password = event.target.password.value
        let confirm_password = event.target.confirm_password.value

        if (password !== confirm_password) {
            setAlert("Password must match confirmed password")
            return
        }

        const requestOptions = {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                username: username,
                section: section,
                password: password,
            })
        }

        fetch(`${developmentBackendLink}/student-register`, requestOptions)
            .then((response) => response.json())
            .then((data) => {
                if (data.error_message) {
                    setAlert(data.error_message)
                    return
                }
                setAlert("Student added successfully")
            })
    }
        
    return (
        <div>
            <br />
            <form method="post" style={{width: "50%", marginLeft: "auto", marginRight: "auto", textAlign: "start"}} onSubmit={registerSubmit}>
                <h1 style={{"textAlign": "center"}}>Register</h1>

                <label htmlFor="username" className="form-label">Username:</label>
                <input type="text" name="username" id="username" placeholder="Enter student's name" className="form-control" />
                
                <br />

                <label htmlFor="password" className="form-label">Section:</label>
                <input type="text" name="password" id="password" placeholder="Enter in this format - 11 Earth" className="form-control" />
                
                <br />

                <label htmlFor="password" className="form-label">Password:</label>
                <input type="text" name="password" id="password" placeholder="Enter student's password" className="form-control" />
                
                <br />

                <label htmlFor="password" className="form-label">Confirm Password:</label>
                <input type="text" name="password" id="confirm_password" placeholder="Confirm student's password" className="form-control" />
                
                <br />

                <button type="submit" className="btn btn-primary">Submit</button>
            </form>
        </div>
    )
}

export default StudentRegisterPage