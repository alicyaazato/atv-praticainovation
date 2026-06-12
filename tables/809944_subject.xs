// Tabela de disciplinas
table subject {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text name? filters=trim
    text professor? filters=trim
    decimal CargaHoraria?
    int user_id? {
      table = "user"
    }
  
    // Situacao da disciplina: rascunho, ativo ou arquivado
    enum status?=ativo {
      values = ["rascunho", "ativo", "arquivado"]
    }
  
    // Periodo/semestre da disciplina, ex: "2026/1"
    text semester? filters=trim
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
    {type: "btree", field: [{name: "status", op: "asc"}]}
  ]
}