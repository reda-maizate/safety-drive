import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:safety_drive_flutter_app_project/screens/Camera.dart';
import 'package:safety_drive_flutter_app_project/screens/Guest.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final List<CameraDescription> cameras = await availableCameras();

  runApp(App(
    cameras: cameras,
  ));
}

class App extends StatelessWidget {
  final List<CameraDescription> cameras;

  App({required this.cameras});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Safety Drive',
      home: GuestScreen(availableCameras: cameras),
    );
  }
}
