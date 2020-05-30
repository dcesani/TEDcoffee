import 'package:flutter/material.dart';
import 'talk_repository.dart';
import 'models/talk.dart';
//tipicamente si divide in più file il main e si importano i vari pezzi
void main() => runApp(MyApp());

class MyApp extends StatelessWidget {
  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TEDcoffee',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: MyHomePage(title: 'TEDcoffee HOME'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  MyHomePage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MyHomePageState createState() => _MyHomePageState();
}
//sono stati
class _MyHomePageState extends State<MyHomePage> {
  final TextEditingController _controller = TextEditingController();
  Future<List<Talk>> _talks;
  int page = 1;

  @override
  void initState() {
    super.initState();
  }
  //metodo asincrono che usa il repository
  //riceve il testo dal controller (casella di testo) e il numero di pagine
  //quando arrivano i risultati, richiamate setState mi permette di fare un refresh dell'interfaccia grafica
  void _getTalksByTag() async {
    setState(() {
      _talks = getTalksByTag(_controller.text, page);
    });
  }

  //è buona norma spezzare questa parte in più file
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TEDcoffee App',
      theme: ThemeData(
        primarySwatch: Colors.red,
      ),
      home: Scaffold( //creo la home vera e propria
        appBar: AppBar( //titolo in alto, sulle slide ci sono esempi per cambiare il colore e i font...
          title: Text('TEDcoffee App'),
        ),
        body: Container(
          alignment: Alignment.center,
          padding: const EdgeInsets.all(8.0),
          child: (_talks == null)
              ? Column( //? = then, layout a colonne
                  mainAxisAlignment: MainAxisAlignment.center, //parte principale
                  children: <Widget>[
                    TextField(
                      controller: _controller,
                      decoration:
                          InputDecoration(hintText: 'Enter your favorite CoffeeTalk'),
                    ),
                    RaisedButton(//pulsanti senza stato
                      child: Text('Search by Tag'),
                      onPressed: () {
                        page = 1;
                        _getTalksByTag();
                      },
                    ),
                  ],
                )
              : FutureBuilder<List<Talk>>( //else
                  future: _talks,
                  builder: (context, snapshot) {
                    if (snapshot.hasData) {
                      return Scaffold(
                          appBar: AppBar(
                            title: Text("#" + _controller.text),
                          ),
                          body: ListView.builder(
                            itemCount: snapshot.data.length,
                            itemBuilder: (context, index) {
                              return GestureDetector( //gestisco le gesture dell'utente
                                child: ListTile(
                                    subtitle:
                                        Text(snapshot.data[index].mainSpeaker),
                                    title: Text(snapshot.data[index].title)),
                                onTap: () => Scaffold.of(context).showSnackBar(
                                    SnackBar(content: Text(snapshot.data[index].details))),
                              );
                            },
                          ),
                          floatingActionButtonLocation://pulsante per la paginazione
                              FloatingActionButtonLocation.centerDocked,
                          floatingActionButton: FloatingActionButton(
                            child: const Icon(Icons.arrow_drop_down), //ci sono molte altre icone da poter usare
                            onPressed: () {
                              if (snapshot.data.length >= 6) {
                                page = page + 1;
                                _getTalksByTag();
                              }
                            },
                          ),
                          bottomNavigationBar: BottomAppBar( //scatta un redrwaw
                            child: new Row(
                              mainAxisSize: MainAxisSize.max,
                              mainAxisAlignment: MainAxisAlignment.spaceBetween,
                              children: <Widget>[
                                IconButton(
                                  icon: Icon(Icons.home),
                                  onPressed: () {
                                    setState(() {
                                      _talks = null;
                                      page = 1;
                                      _controller.text = "";
                                    });
                                  },
                                )
                              ],
                            ),
                          ));
                    } else if (snapshot.hasError) {
                      return Text("${snapshot.error}");
                    }

                    return CircularProgressIndicator();
                  },
                ),
        ),
      ),
    );
  }
}
