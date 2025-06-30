package app

import "database/sql"

type Application struct {
	ProductionFrontendLink  string
	DevelopmentFrontendLink string
	DatabaseDSN             string
	Deployed                bool
	Port                    string
	DB                      *sql.DB
}
