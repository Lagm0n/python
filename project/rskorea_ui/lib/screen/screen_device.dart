import 'dart:convert';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:rskorea_ui/model/model_gasdata.dart';
import 'package:rskorea_ui/widget/widget_deviceInfo.dart';
import 'package:http/http.dart' as http;

import '../function.dart';

class DeviceScreen extends StatefulWidget {
  String name;
  String address;

  DeviceScreen({required this.name, required this.address});

  @override
  State<DeviceScreen> createState() => _DeviceScreenState();
}

class _DeviceScreenState extends State<DeviceScreen> {
  bool isConneted = false;
  String info = 'http://10.0.2.2:5000/info';
  String value = 'http://10.0.2.2:5000/value';
  dynamic data;
  int gasCount = 0;
  List gasBeanList = [];
  List gasValueList = [];
  bool isLoading = false;
  String dataStatus = '';

  @override
  void initState() {
    super.initState();
    sendData();
  }

  Future<void> sendData() async {
    var postStatus = await fetchdata(info, 'POST', sendData: widget.address);
    setState(() {
      // ignore: unrelated_type_equality_checks
      if (postStatus == 200) {
        isLoading = true;
      } else {
        isLoading = false;
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width;
    double height = screenSize.height;

    DateTime now = DateTime.now();
    DateTime currentTime =
        DateTime(now.year, now.month, now.day, now.hour, now.minute);
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
            title: Text(widget.name),
            backgroundColor: Colors.blueAccent,
            automaticallyImplyLeading: false,
            actions: [
              TextButton(
                style: TextButton.styleFrom(
                  textStyle: TextStyle(
                      fontSize: width * 0.05,
                      fontWeight: FontWeight.bold,
                      color: Colors.white),
                ),
                onPressed: null,
                child: const Text('Disconnect'),
              ),
            ]),
        body: isLoading == false
            ? const Center(child: CircularProgressIndicator())
            : Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Padding(
                    padding: EdgeInsets.only(top: width * 0.05),
                  ),
                  InfoLabelWidget(
                    text: '연결 시간 :',
                    variable: '$currentTime',
                  ),
                  gasCount == 0
                      ? Container()
                      : InfoLabelWidget(
                          text: '가수 수 :',
                          variable: '$gasCount',
                        ),
                  Expanded(
                    child: ListView.builder(
                        // ignore: unnecessary_null_comparison
                        itemCount: gasBeanList == null ? 0 : gasBeanList.length,
                        itemBuilder: (context, index) {
                          return Column(
                            children: [
                              const SizedBox(
                                height: 4,
                              ),
                              InfoLabelWidget(
                                  text:
                                      '${gasBeanList[index]['Gas']['name']} - ${gasBeanList[index]['Unit']['name']}',
                                  variable: '')
                            ],
                          );
                        }),
                  ),
                  Expanded(
                    child: ListView.builder(
                        // ignore: unnecessary_null_comparison
                        itemCount:
                            gasValueList == null ? 0 : gasValueList.length,
                        itemBuilder: (context, index) {
                          return gasValueList == null
                              ? Container()
                              : Column(
                                  children: [
                                    const SizedBox(
                                      height: 4,
                                    ),
                                    InfoLabelWidget(
                                        text:
                                            '${gasBeanList[index]['Gas']['name']} : ${gasValueList[index]} ${gasBeanList[index]['Unit']['name']}',
                                        variable: '')
                                  ],
                                );
                        }),
                  ),
                ],
              ),
        bottomNavigationBar: isLoading == false
            ? null
            : Padding(
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
                            data = await fetchdata(info, 'GET');
                            var response = jsonDecode(data);
                            setState(() {
                              gasBeanList = response['gasBeanList'];
                              gasCount = response['gasCount'];
                            });
                          },
                          child: const Text('show GasType'),
                        )
                      ]),
                    ),
                    const SizedBox(
                      height: 4,
                      width: 10,
                    ),
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
                            data = await fetchdata(value, 'GET');
                            var response = jsonDecode(data);
                            setState(() {
                              gasValueList = response['gasValueList'];
                            });
                          },
                          child: const Text('show GasData'),
                        )
                      ]),
                    ),
                  ],
                ),
              ),
      ),
    );
  }
}
