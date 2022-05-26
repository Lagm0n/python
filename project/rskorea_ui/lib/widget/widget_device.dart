import 'package:flutter/material.dart';

class DeviceWidget extends StatefulWidget {
  String name;
  String address;
  double width;
  VoidCallback tap;

  DeviceWidget(
      {required this.name,
      required this.address,
      required this.width,
      required this.tap});

  @override
  State<DeviceWidget> createState() => _DeviceWidgetState();
}

class _DeviceWidgetState extends State<DeviceWidget> {
  @override
  Widget build(BuildContext context) {
    return Container(
      width: widget.width,
      height: widget.width * 0.1,
      padding: EdgeInsets.fromLTRB(widget.width * 0.02, widget.width * 0.01,
          widget.width * 0.02, widget.width * 0.01),
      decoration: BoxDecoration(
          border: Border.all(color: Colors.blue, width: 3),
          borderRadius: BorderRadius.circular(15)),
      child: InkWell(
        child: Row(
          children: [
            Text(
              widget.name,
              style: TextStyle(
                  fontSize: widget.width * 0.05,
                  fontWeight: FontWeight.bold,
                  color: Colors.black),
            ),
            const Padding(
              padding: EdgeInsets.all(10),
            ),
            Text(
              widget.address,
              style: TextStyle(
                  fontSize: widget.width * 0.03,
                  fontWeight: FontWeight.bold,
                  color: Colors.grey),
            ),
          ],
        ),
        onTap: () {
          widget.tap();
        },
      ),
    );
  }
}
