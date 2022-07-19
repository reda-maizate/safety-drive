import 'dart:io';
import 'package:aws_s3_plugin_flutter/aws_s3_plugin_flutter.dart';
import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:safety_drive_flutter_app_project/db/UserModel.dart';
import 'package:safety_drive_flutter_app_project/screens/Guest.dart';

class CameraScreen extends StatefulWidget {
  final UserModel userModel;
  final List<CameraDescription> availableCameras;

  const CameraScreen({
    Key? key,
    required this.userModel,
    required this.availableCameras,
  })
      : super(key: key);

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late Future<void> _initializeControllerFuture;
  late CameraController _cameraController;
  bool _isRecording = false;
  bool _stopingInProgress = true;
  int _selectedCameraIndex = 1;
  Icon videoIcon = const Icon(
    Icons.videocam,
    color: Colors.black,
  );

  @override
  void dispose() {
    _cameraController.dispose();
    super.dispose();
  }

  Future<void> initCamera(CameraDescription camera) async {
    _cameraController = CameraController(
      camera,
      ResolutionPreset.max,
    );

    _cameraController.addListener(() {
      if (mounted) {
        setState(() {});
      }
    });

    if (_cameraController.value.hasError) {
      print('Camera Error ${_cameraController.value.errorDescription}');
    }

    _initializeControllerFuture = _cameraController.initialize();

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _cameraToggle() async {
    setState(() {
      _selectedCameraIndex = _selectedCameraIndex == 0 ? 1 : 0;
    });

    await initCamera(widget.availableCameras[_selectedCameraIndex]);
  }

  @override
  void initState() {
    super.initState();

    _cameraToggle();
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: FutureBuilder(
          future: _initializeControllerFuture,
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.done) {
              return Stack(
                children: [
                  // Transform.scale(
                  //   scale: 1 / _controller.value.aspectRatio,
                  //   child: Center(
                  //     child: AspectRatio(
                  //       aspectRatio: _controller.value.aspectRatio,
                  //       child: CameraPreview(_controller),
                  //     ),
                  //   ),
                  // ),
                  CameraPreview(_cameraController),
                  Positioned(
                    left: 30,
                    top: 30,
                    child: Container(
                      height: 50.0,
                      width: 50.0,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(
                          width: 3.0,
                        ),
                      ),
                      child: Material(
                        color: Colors.transparent,
                        child: InkWell(
                          customBorder: const CircleBorder(),
                          onTap: () {
                            Navigator.push(
                              context,
                              MaterialPageRoute(
                                builder: (context) => GuestScreen(
                                    availableCameras: widget.availableCameras),
                              ),
                            );
                          },
                          child: const Icon(
                            Icons.arrow_back,
                          ),
                        ),
                      ),
                    ),
                  ),
                  Positioned(
                    right: 30,
                    top: 30,
                    child: Container(
                      height: 50.0,
                      width: 50.0,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        border: Border.all(
                          width: 3.0,
                        ),
                      ),
                      child: Material(
                        color: Colors.transparent,
                        child: InkWell(
                          customBorder: const CircleBorder(),
                          onTap: () => _cameraToggle(),
                          child: const Icon(
                            Icons.loop,
                          ),
                        ),
                      ),
                    ),
                  ),
                ],
              );
            }

            return const Center(
              child: Text('camera'),
            );
          },
        ),
        floatingActionButton: Container(
          margin: const EdgeInsets.only(
            bottom: 20.0,
          ),
          decoration: BoxDecoration(
            shape: BoxShape.circle,
            border: Border.all(
              width: 3.0,
            ),
          ),
          child: FittedBox(
            child: InkWell(
              child: FloatingActionButton(
                onPressed: () {
                  _stopingInProgress = !_stopingInProgress;
                  setState(() {
                    if (_stopingInProgress) {
                      videoIcon = const Icon(
                        Icons.videocam,
                        color: Colors.black,
                      );
                    } else {
                      videoIcon = const Icon(
                        Icons.stop,
                        color: Colors.red,
                      );
                    }
                  });
                  // _takeVideo(_isRecorded);
                  if (!_isRecording) {
                    recordVideo();
                  }
                },
                backgroundColor: Colors.transparent,
                elevation: 0.0,
                child: videoIcon,
              ),
            ),
          ),
        ),
        floatingActionButtonLocation: FloatingActionButtonLocation.centerFloat,
      ),
    );
  }

  Future<void> recordVideo() async {
    if (!_stopingInProgress) {
      // _availableCameras ??= await availableCameras();
      _cameraController = CameraController(
        widget.availableCameras[_selectedCameraIndex],
        ResolutionPreset.max,
      );
      await _cameraController.initialize();
      await _cameraController.startVideoRecording();
      setState(() {
        _isRecording = true;
      });

      await Future.delayed(const Duration(seconds: 2), () {});
    }

    if (_isRecording) {
      XFile xfile = await _cameraController.stopVideoRecording();

      File file = File(xfile.path);

      String pathVideo = 'cameravideo_${widget.userModel.uid}.avi';

      AwsS3PluginFlutter awsS3 = AwsS3PluginFlutter(
        file: file,
        fileNameWithExt: pathVideo,
        awsFolderPath: '',
        bucketName: 'safety-drive-bucket',
        AWSAccess: '',
        AWSSecret: '',
        region: Regions.US_EAST_1,
      );

      var result = await awsS3.uploadFile;
      debugPrint("Result :'$result'.");

      setState(() {
        _isRecording = false;
      });

      recordVideo();
    }
  }
}
