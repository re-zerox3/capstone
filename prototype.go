package main

import(
				"net/http"
				"html/template"
				"fmt"
				"log"
)

func errEx(err error){
				if err != nil{
								log.Fatal(err)
				}
}


func Home(writer http.ResponseWriter, request *http.Request){
				html, err := template.ParseFiles("home.html")
				errEx(err)
				html.Execute(writer, nil)
}

func Inspection(writer http.ResponseWriter, request *http.Request){
				html, err := template.ParseFiles("inspectionForm.html")
				errEx(err)
				html.Execute(writer, nil)
}


func Mileage1(writer http.ResponseWriter, request *http.Request){
				html, err := template.ParseFiles("mileage_1.html")
				errEx(err)
				html.Execute(writer,nil)
}


func Mileage2(writer http.ResponseWriter, request *http.Request){
				html, err := template.ParseFiles("mileage_2.html")
				errEx(err)
				html.Execute(writer,nil)
}

func Tsvr(writer http.ResponseWriter, request *http.Request){
				html, err := template.ParseFiles("TSVR_Form.html")
				errEx(err)
				html.Execute(writer,nil)
}

func main(){
				fmt.Println("hello world")
				http.HandleFunc("/",Home)
				http.HandleFunc("/inspection",Inspection)
				http.HandleFunc("/mileage1",Mileage1)
				http.HandleFunc("/mileage2",Mileage2)
				http.HandleFunc("/tsvr",Tsvr)
				http.ListenAndServe("localhost:5000",nil)
}
