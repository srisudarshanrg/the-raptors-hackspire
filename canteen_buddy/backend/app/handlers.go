package app

import (
	"fmt"
	"net/http"
)

func (app *Application) Home(w http.ResponseWriter, r *http.Request) {
	fmt.Fprint(w, "Application running")
}

func (app *Application) Login(w http.ResponseWriter, r *http.Request) {

}

func (app *Application) Register(w http.ResponseWriter, r *http.Request) {

}
