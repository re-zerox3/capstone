package main

import(
				"net/http"
				"html/template"
				"fmt"
				"log"
				"database/sql"	
				_ "github.com/mattn/go-sqlite3"

)

func errEx(err error){
				if err != nil{
								log.Fatal(err)
				}
}




func Connect() *sql.DB {
				db, err := sql.Open("sqlite3", "./databaseForm.sqlite")
				if err != nil{	
								http.Redirect(nil,nil, "/error404",http.StatusFound)
								fmt.Println("what------------------------")
				}
				fmt.Println("--------------------end error-----------")
				return db
}


func main(){
				fmt.Println("Hello World")
}
