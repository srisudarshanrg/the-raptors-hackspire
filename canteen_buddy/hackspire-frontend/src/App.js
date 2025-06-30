import { useState } from 'react';
import './App.css';
import { Outlet } from 'react-router-dom';

function App() {
  const [login, setLogin] = useState(false);
  const [canteenLogin, setCanteenLogin] = useState(false);
  const [teacherLogin, setTeacherLogin] = useState(false);
  const [alert, setAlert] = useState(null);
  const developmentBackendLink = "http://localhost:3500"
  const productionBackendLink = ""

  const alertShow = () => {
    return (
      <div class="alert alert-primary alert-dismissible fade show" role="alert">
        {alert}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>
    )
  }

  return (
    <div className="App">
      <nav class="navbar navbar-expand-lg bg-dark" data-bs-theme="dark">
        <div class="container-fluid">
          <a class="navbar-brand" href="#">The Raptors</a>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
              <li class="nav-item">
                <a class="nav-link" aria-current="page" href="/">Home</a>
              </li>
              {login && (
                <>
                  <li class="nav-item">
                    <a class="nav-link" href="/canteen-buddy">Canteen Buddy</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" href="/menu">Assignment Tracker</a>
                  </li>
                </>
              )}

              {canteenLogin && (
                <>
                  <li class="nav-item">
                    <a class="nav-link" aria-current="page" href="/view-orders">View Orders</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" aria-current="page" href="/update-menu">Update Menu</a>
                  </li>
                </>
              )}

              {teacherLogin && (
                <>
                  <li class="nav-item">
                    <a class="nav-link" aria-current="page" href="/teacher-logout">View Assignments</a>
                  </li>
                  <li class="nav-item">
                    <a class="nav-link" aria-current="page" href="/teacher-logout">Teacher Logout</a>
                  </li>
                </>
              )}
              
            </ul>
          </div>
            
          {!canteenLogin && !login && !teacherLogin && (
            <div class="navbar-nav" id="navbarNav">
              <ul class="navbar-nav"> 
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/student-login">Student Login</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/student-register">Student Register</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/canteen-login">Canteen Login</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/teacher-login">Teacher Login</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/teacher-login">Teacher Register</a>
                </li>
              </ul>
            </div>
          )}

          {canteenLogin && (
            <div className="navbar-nav" id="navbarNav">
              <ul className="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/canteen-logout">Canteen Logout</a>
                </li>
              </ul>
            </div>
          )}

          {login && (
            <div className="navbar-nav" id="navbarNav">
              <ul className="navbar-nav">
                <li class="nav-item">
                  <a class="nav-link" aria-current="page" href="/student-logout">Logout</a>
                </li>
              </ul>
            </div>
          )}          
        </div>
      </nav>

      {alert !== null && alertShow()}

      <Outlet
        context={{
          developmentBackendLink,
          productionBackendLink,
          login,
          setLogin,
          canteenLogin,
          setCanteenLogin,
          teacherLogin,
          setTeacherLogin,
          alert,
          setAlert,
        }}
      />

    </div>
  );
}

export default App;
