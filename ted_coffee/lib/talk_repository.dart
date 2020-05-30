import 'package:http/http.dart' as http; //per la chiamata
import 'dart:convert'; //devo convertire i JSON in una JSONmap
import 'models/talk.dart'; //modello dati

//richiamo i dati in maniera asincrona, per questo usa una FutureList perchè mi permette di fare un appen di quelli che arrivano dopo
Future<List<Talk>> getTalksByTag(String tag, int page) async {
  final String url =
      'https://qq8e0745w0.execute-api.us-east-1.amazonaws.com/default/Get_Talks_By_Tag';

    //API esposta tramite metodo post
  final http.Response response = await http.post(url,
    headers: <String, String>{
      'Content-Type': 'application/json; charset=UTF-8',
    },
    body: jsonEncode(<String, Object>{
      'tag': tag,
      'page': page,
      'doc_per_page': 6 //sarebbe meglio vedere quanti documenti ci sono e variare questo parametro sulla base del layout dell'applicazione
    }),
  );
  if (response.statusCode == 200) { //potrei gestire diversi statusCode
    Iterable list = json.decode(response.body);
    var talks = list.map((model) => Talk.fromJSON(model)).toList();//metodo statico
    return talks;
  } else {
    throw Exception('Failed to load talks');
  }
      
}
