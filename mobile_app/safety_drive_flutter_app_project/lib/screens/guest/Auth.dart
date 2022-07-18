import 'package:flutter/material.dart';
import 'package:safety_drive_flutter_app_project/services/UserService.dart';

class AuthScreen extends StatefulWidget {
  final Function(int, String) onChangedStep;

  const AuthScreen({
    Key? key,
    required this.onChangedStep,
  }) : super(key: key);

  @override
  State<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends State<AuthScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final RegExp regex_email = RegExp(r"[a-z0-9\._-]+@[a-z0-9\._-]+\.[a-z]+");

  String _email = '';

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        body: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(
              horizontal: 30.0,
            ),
            child: Column(
              children: [
                Text(
                  "Safety Drive".toUpperCase(),
                  style: TextStyle(
                    fontSize: 30.0,
                    color: Theme.of(context).primaryColor,
                  ),
                ),
                const SizedBox(
                  height: 150.0,
                ),
                Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      Text("Enter your email"),
                      const SizedBox(
                        height: 5.0,
                      ),
                      TextFormField(
                        onChanged: (value) => setState(() => _email = value),
                        validator: (value) {
                          if (value == null ||
                              value.isEmpty ||
                              value.length > 128) {
                            'Enter a email with 128 caracters max';
                          } else {
                            !regex_email.hasMatch(value)
                                ? 'Enter a valid email'
                                : null;
                          }
                        },
                        decoration: const InputDecoration(
                          hintText: 'Example : email@domain.com',
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(
                        height: 10.0,
                      ),
                      ElevatedButton(
                        onPressed: () async {
                          if (_formKey.currentState!.validate()) {
                            widget.onChangedStep(1, _email);
                          }
                        },
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 15.0),
                          child: Text(
                            'Next'.toUpperCase(),
                          ),
                        ),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        ),
      ),
    );
  }
}
