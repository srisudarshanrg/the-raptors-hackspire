package main

import (
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/joho/godotenv"
	"github.com/srisudarshanrg/the-raptors-hackspire/canteen_buddy/app"
)

func main() {
	godotenv.Load(".env")
	port := os.Getenv("PORT")
	dbPassword := os.Getenv("DATABASE_PASSWORD")

	log.Println("Port:", port)

	var app app.Application

	app.Deployed = false
	app.DatabaseDSN = fmt.Sprintf("host=postgresql-raptor.alwaysdata.net dbname=raptor_hackspire port=5432 user=raptor password=%s", dbPassword)
	app.DevelopmentFrontendLink = "http://localhost:3000"
	app.ProductionFrontendLink = ""

	if app.Deployed {
		app.Port = fmt.Sprintf("0.0.0.0:%s", port)
	} else {
		app.Port = fmt.Sprintf("localhost:%s", port)
	}

	log.Println("Connecting to database...")
	db, err := app.ConnectDB()
	if err != nil {
		log.Fatal(err)
		return
	}

	log.Println("Connected to database")
	app.DB = db
	defer db.Close()

	log.Println("Application running")
	http.ListenAndServe(app.Port, app.Routes())
}
