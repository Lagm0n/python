import 'package:flutter/material.dart';
import 'dart:convert';

import 'package:rskorea_ui/function.dart';
import 'package:rskorea_ui/screen/screen_device.dart';
import 'package:rskorea_ui/widget/widget_device.dart';

class HomeScreen extends StatefulWidget {
  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  bool isConneted = false;
  String url = 'http://10.0.2.2:5000/scan';
  dynamic data;
  int len = 0;
  List bleList = [];
  @override
  Widget build(BuildContext context) {
    Size size = MediaQuery.of(context).size;
    double width = size.width;
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(title: Text("Rs korea")),
        body: ListView.builder(
            itemCount: bleList == null ? 0 : bleList.length,
            itemBuilder: (context, index) {
              var name = bleList[index]['name'];
              var address = bleList[index]['address'];
              return Column(
                children: [
                  const SizedBox(
                    height: 4,
                  ),
                  DeviceWidget(
                    name: name ?? 'unknown',
                    address: address,
                    width: width,
                    tap: () async {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (context) => DeviceScreen(
                              name: name ?? 'unknown', address: address),
                        ),
                      );
                    },
                  ),
                ],
              );
            }),
        bottomNavigationBar: Padding(
          padding: const EdgeInsets.all(8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              ClipRRect(
                borderRadius: BorderRadius.circular(4),
                child: Stack(children: [
                  Positioned.fill(
                    child: Container(
                      width: width,
                      decoration: const BoxDecoration(
                        gradient: LinearGradient(
                          colors: <Color>[
                            Color(0xFF0D47A1),
                            Color(0xFF1976D2),
                            Color(0xFF42A5F5),
                          ],
                        ),
                      ),
                    ),
                  ),
                  TextButton(
                    style: TextButton.styleFrom(
                      padding: const EdgeInsets.all(16),
                      primary: Colors.white,
                      textStyle: const TextStyle(
                        fontSize: 20,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                    onPressed: () async {
                      data = await fetchdata(url, 'GET');
                      var response = jsonDecode(data);
                      setState(() {
                        len = response['len'];
                        bleList = response['bluetoothList'];
                      });
                    },
                    child: const Text('Bluetooth Scan'),
                  )
                ]),
              ),
              const SizedBox(height: 4)
            ],
          ),
        ),
      ),
    );
  }
}
