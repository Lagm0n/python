import 'package:http/http.dart' as http;

fetchdata(String url, String type, {dynamic sendData}) async {
  if (type == 'GET') {
    http.Response response = await http.get(Uri.parse(url));
    return response.body;
  } else if (type == 'POST') {
    http.Response response = await http.post(Uri.parse(url), body: sendData);
    return response.statusCode;
  }
}
