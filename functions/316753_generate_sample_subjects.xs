// Função para gerar registros de disciplinas de exemplo
// Gera registros de exemplo na tabela subject com nome da materia, professor e carga horaria
function generate_sample_subjects {
  input {
  }

  stack {
    // Lista de disciplinas para inserção
    var $data_to_insert {
      value = [
        { name: "Cálculo I", professor: "Dr. Newton", CargaHoraria: 60.0 }
        { name: "Física Geral", professor: "Albert Einstein", CargaHoraria: 45.0 }
        { name: "Programação XanoScript", professor: "Xano Developer", CargaHoraria: 80.0 }
        { name: "Banco de Dados", professor: "Grace Hopper", CargaHoraria: 40.0 }
        { name: "Inteligência Artificial", professor: "Alan Turing", CargaHoraria: 50.0 }
      ]
    }
  
    var $inserted_list {
      value = []
    }
  
    // Inserindo os registros individualmente
    foreach ($data_to_insert) {
      each as $item {
        db.add subject {
          enforce_hidden_fields = false
          data = {
            name        : $item.name
            professor   : $item.professor
            CargaHoraria: $item.CargaHoraria
            user_id     : null
            created_at  : now
          }
        } as $new_record
      
        // Adicionando o registro criado à lista de resultados usando filtro push
        var.update $inserted_list {
          value = $inserted_list|push:$new_record
        }
      }
    }
  }

  response = $inserted_list
}