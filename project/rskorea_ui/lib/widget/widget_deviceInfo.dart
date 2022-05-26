import 'package:flutter/material.dart';

class InfoLabelWidget extends StatefulWidget {
  String text;
  String variable;

  InfoLabelWidget({required this.text, required this.variable});

  @override
  State<InfoLabelWidget> createState() => _InfoLabelWidgetState();
}

class _InfoLabelWidgetState extends State<InfoLabelWidget> {
  @override
  Widget build(BuildContext context) {
    Size screenSize = MediaQuery.of(context).size;
    double width = screenSize.width;
    return Row(
      children: [
        Padding(
          padding: EdgeInsets.fromLTRB(
              width * 0.02, width * 0.01, width * 0.02, width * 0.01),
        ),
        Text(
          widget.text,
          style: TextStyle(
              fontSize: width * 0.05,
              fontWeight: FontWeight.bold,
              color: Colors.black),
        ),
        Padding(
          padding: EdgeInsets.only(left: width * 0.05, right: width * 0.05),
        ),
        Text(
          widget.variable,
          style: TextStyle(
              fontSize: width * 0.05,
              fontWeight: FontWeight.bold,
              color: Colors.black),
        ),
      ],
    );
  }
}
