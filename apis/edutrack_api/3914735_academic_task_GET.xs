// Query all academic_task records
query academic_task verb=GET {
  api_group = "edutrackAPI"

  input {
  }

  stack {
    db.query academic_task {
      return = {type: "list"}
    } as $model
  }

  response = $model
}