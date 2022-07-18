import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:crypto/crypto.dart';

class SignUpScreen extends StatefulWidget {
  final Function(int? index, String? pseudo, String? password) onChangedStep;

  const SignUpScreen({
    Key? key,
    required this.onChangedStep,
  }) : super(key: key);

  @override
  State<SignUpScreen> createState() => _SignUpScreenState();
}

class _SignUpScreenState extends State<SignUpScreen> {
  final GlobalKey<FormState> _formKey = GlobalKey<FormState>();
  final RegExp regex_password = RegExp(r"[a-z0-9\._-]+");

  bool _isSecret = true;
  String _pseudo = '';
  String _password = '';

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          leading: IconButton(
            icon: const Icon(Icons.arrow_back),
            onPressed: () => widget.onChangedStep(1, null, null),
          ),
        ),
        body: Center(
          child: SingleChildScrollView(
            padding: const EdgeInsets.symmetric(
              horizontal: 30.0,
            ),
            child: Column(
              children: [
                Text(
                  'Sign Up'.toUpperCase(),
                  style: const TextStyle(
                    fontSize: 30.0,
                  ),
                ),
                const SizedBox(
                  height: 50.0,
                ),
                Form(
                  key: _formKey,
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const Text("Enter your Pseudo"),
                      const SizedBox(
                        height: 5.0,
                      ),
                      TextFormField(
                        onChanged: (value) => setState(() => _pseudo = value),
                        validator: (value) {
                          if (value == null || value.length < 6 || value.length > 128) {
                            return 'Enter a pseudo with 6 caracters min and 128 caracters max';
                          } else {
                            return !regex_password.hasMatch(value)
                                ? 'Your pseudo can only contain [a-z0-9\._-] caracters+'
                                : null;
                          }
                        },
                        decoration: const InputDecoration(
                          hintText: 'Example : MyPseudo',
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(
                        height: 10.0,
                      ),
                      const Text("Enter your Password"),
                      const SizedBox(
                        height: 5.0,
                      ),
                      TextFormField(
                        onChanged: (value) => setState(() =>
                            _password = sha512.convert(utf8.encode(value)).toString()),
                        validator: (value) {
                          if (value == null || value.length < 8) {
                            return 'Enter a password with 8 caracters min';
                          } else {
                            return !regex_password.hasMatch(value)
                                ? 'Your password can only contain [a-z0-9\._-] caracters+'
                                : null;
                          }
                        },
                        obscureText: _isSecret,
                        decoration: InputDecoration(
                          suffixIcon: InkWell(
                            onTap: () => setState(() => _isSecret = !_isSecret),
                            child: Icon(!_isSecret
                                ? Icons.visibility
                                : Icons.visibility_off),
                          ),
                          hintText: 'Example : dF41GL7u',
                          border: OutlineInputBorder(),
                        ),
                      ),
                      const SizedBox(
                        height: 10.0,
                      ),
                      ElevatedButton(
                        onPressed: () {
                          if (_formKey.currentState!.validate()) {
                            print(_password);
                            widget.onChangedStep(null, _pseudo, _password);
                          }
                        },
                        child: Padding(
                          padding: const EdgeInsets.symmetric(vertical: 15.0),
                          child: Text(
                            'Sign Up'.toUpperCase(),
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
