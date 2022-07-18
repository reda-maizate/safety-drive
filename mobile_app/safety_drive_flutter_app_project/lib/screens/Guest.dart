import 'package:flutter/material.dart';
import 'package:safety_drive_flutter_app_project/screens/Home.dart';
import 'package:safety_drive_flutter_app_project/screens/guest/Auth.dart';
import 'package:safety_drive_flutter_app_project/screens/guest/SignIn.dart';
import 'package:safety_drive_flutter_app_project/screens/guest/SignUp.dart';
import 'package:safety_drive_flutter_app_project/screens/guest/Term.dart';
import 'package:safety_drive_flutter_app_project/services/UserService.dart';

class GuestScreen extends StatefulWidget {
  const GuestScreen({Key? key}) : super(key: key);

  @override
  State<GuestScreen> createState() => _GuestScreenState();
}

class _GuestScreenState extends State<GuestScreen> {
  final UserService _userService = UserService();
  final List<Widget> _widgets = [];
  int _indexSelected = 0;

  String? _email;
  String? _pseudo;
  String? _password;

  @override
  void initState() {
    super.initState();

    _widgets.addAll([
      AuthScreen(
        onChangedStep: (index, email) async {
          await _userService.emailExisted(email).then((value) {
          setState(() {
            if (value) {
              _indexSelected = index + 2;
            } else {
              _indexSelected = index;
            }
            _email = email;
          });});
        },
      ),
      TermScreen(
        onChangedStep: (index) => setState(() => _indexSelected = index),
      ),
      SignUpScreen(
        onChangedStep: (index, pseudo, password) => setState(() {
          if (index != null) {
            _indexSelected = index;
          }

          if (pseudo != null && password != null) {
            _pseudo = pseudo;
            _password = password;
            _userService
                .signUp(
              _email.toString(),
              _pseudo.toString(),
              _password.toString(),
            )
                .then((value) {
              if (value != null) {
                // Navigator.push(
                  // context,
                  // MaterialPageRoute(
                    // builder: (context) => HomeScreen(),
                  // ),
                // );
              }
            });
          }
        }),
      ),
      SignInScreen(
        onChangedStep: (index, password) => setState(() {
          if (index != null) {
            _indexSelected = index;
          }

          if (password != null) {
            _password = password;
            _userService
                .signIn(
              _email.toString(),
              _password.toString(),
            )
                .then((value) {
              if (value != null) {
                // Navigator.push(
                //   context,
                //   MaterialPageRoute(
                //     builder: (context) => HomeScreen(),
                //   ),
                // );
              }
            });
          }
        }),
      ),
    ]);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: _widgets.isEmpty
          ? const SafeArea(
              child: Scaffold(
                body: Center(
                  child: Text('Loading...'),
                ),
              ),
            )
          : _widgets.elementAt(_indexSelected),
    );
  }
}
