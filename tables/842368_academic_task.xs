table academic_task {
  auth = false

  schema {
    // Unique identifier for the academic task
    int id
  
    // Timestamp when the task was created
    timestamp created_at?=now
  
    // Timestamp when the task was last updated
    timestamp updated_at?=now
  
    // Reference to the student (user) who owns this task
    int user_id {
      table = "user"
    }
  
    // Reference to the subject this task is linked to
    int subject_id {
      table = "subject"
    }
  
    // Title of the academic task (max 255 characters)
    text title filters=trim|max:255
  
    // Optional detailed description of the task
    text description? filters=trim
  
    // Current status of the task, defaults to pending
    enum status?=Pendente {
      values = ["Pendente", "Em_progresso", "Completa", "Atrasada"]
    }
  
    text data filters=trim
  
    // Prioridade da tarefa, default Media
    enum priority?=Media {
      values = ["Baixa", "Media", "Alta"]
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "updated_at", op: "desc"}]}
    {type: "btree", field: [{name: "user_id", op: "asc"}]}
    {type: "btree", field: [{name: "subject_id", op: "asc"}]}
    {type: "btree", field: [{name: "status", op: "asc"}]}
    {type: "btree", field: [{name: "priority", op: "asc"}]}
    {
      type : "btree"
      field: [{name: "user_id", op: "asc"}, {name: "status", op: "asc"}]
    }
  ]
}