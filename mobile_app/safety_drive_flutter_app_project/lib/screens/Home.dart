import 'dart:async';
import 'dart:io';
import 'dart:ui';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';

class HomeScreen extends StatelessWidget {
  final String imagePath;

  const HomeScreen({super.key, required this.imagePath});

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Image.file(File(imagePath)),
      ),
    );
  }
}