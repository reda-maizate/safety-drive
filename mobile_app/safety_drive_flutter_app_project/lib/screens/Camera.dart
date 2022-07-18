import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:safety_drive_flutter_app_project/screens/Home.dart';

class CameraScreen extends StatefulWidget {
  List<CameraDescription> cameras = <CameraDescription>[];

  CameraScreen({
    Key? key,
    required this.cameras,
  }) : super(key: key);

  @override
  State<CameraScreen> createState() => _CameraScreenState();
}

class _CameraScreenState extends State<CameraScreen> {
  late Future<void> _initializeControllerFuture;
  late CameraController _controller;
  int _selectedCameraIndex = -1;
  Icon videoIcon = const Icon(
    Icons.videocam,
    color: Colors.black,
  );
  bool _isRecorded = false;

  Future<void> initCamera(CameraDescription camera) async {
    _controller = CameraController(
      camera,
      ResolutionPreset.medium,
      imageFormatGroup: ImageFormatGroup.yuv420,
    );

    _controller.addListener(() {
      if (mounted) {
        setState(() {});
      }
    });

    if (_controller.value.hasError) {
      print('Camera Error ${_controller.value.errorDescription}');
    }

    _initializeControllerFuture = _controller.initialize();

    if (mounted) {
      setState(() {});
    }
  }

  Future<void> _cameraToggle() async {
    setState(() {
      _selectedCameraIndex = _selectedCameraIndex > -1
          ? _selectedCameraIndex == 0
              ? 1
              : 0
          : 0;
    });

    await initCamera(widget.cameras[_selectedCameraIndex]);
  }

  // Future<void> _takePhoto() async {
    
  // }

  Future<void> _takeVideo(bool isReccorded) async {
    try {
      await _initializeControllerFuture;

      final String pathVideo = join((await getTemporaryDirectory()).path,
          's{DateTime.now().millisecondsSinceEpoch}.avi');
      
      print(_controller);
      if (isReccorded) {
        print(_controller);
        await _controller.startVideoRecording();
      } else {
        XFile video = await _controller.stopVideoRecording();
        print(video);
        // await video.saveTo(pathVideo);
      }
      print(pathVideo);
    } catch (e) {
      print(e);
    }
  }

  @override
  void initState() {
    super.initState();

    _cameraToggle();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
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
                  CameraPreview(_controller),
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
                          onTap: () => print('retour'),
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
                onPressed: () async {
                  _isRecorded = !_isRecorded;
                  setState(() {
                    if (!_isRecorded) {
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
                  try {
                    await _initializeControllerFuture;

                    var path = await _controller.takePicture();
                    print(path.path);

                    await Navigator.push(context,
                      MaterialPageRoute(
                        builder: (context) => HomeScreen(imagePath: path.path),
                      ),
                    );
                  } catch(e) {
                    print(e);
                  }
                  // _takeVideo(_isRecorded);
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
}
