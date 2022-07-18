import 'dart:convert';
import 'package:crypto/crypto.dart';
import 'package:safety_drive_flutter_app_project/db/Mysql.dart';
import 'package:safety_drive_flutter_app_project/db/UserModel.dart';

class UserService {
  final Mysql _db = Mysql();

  Future<UserModel?> signUp(
      String email, String pseudo, String password) async {
    try {
      await _db.getConnection().then((conn) async {
        await conn.query(
            'INSERT INTO USERS (id_user, email, password, pseudo) VALUES (?, ?, ?, ?)',
            [
              sha512.convert(utf8.encode(email)).toString(),
              email,
              password,
              pseudo,
            ]);
        conn.close();
      });
      return UserModel(
        uid: sha512.convert(utf8.encode(email)).toString(),
        email: email,
        password: password,
        pseudo: pseudo,
      );
    } catch (e) {
      return null;
    }
  }

  Future<bool> emailExisted(String email) async {
    var res = false;
    await _db.getConnection().then((conn) async {
      var result = await conn.query('SELECT * FROM USERS WHERE email = ?', [
        email,
      ]);
      conn.close();
      if (result.isNotEmpty) {
        res = true;
      }
    });
    return res;
  }

  Future<UserModel?> signIn(String email, String password) async {
    UserModel? userModel = null;
    await _db.getConnection().then((conn) async {
      await conn.query('SELECT * FROM USERS WHERE email = ? AND password = ?', [
        email,
        password,
      ]).then((result) {
        if (result.isNotEmpty) {
          for (var res in result) {
            conn.close();
            userModel = UserModel(
              uid: res['user_id'].toString(),
              email: email,
              password: password,
              pseudo: res['pseudo'].toString(),
            );
          }
        }
      });
      conn.close();
    });
    return userModel;
  }
}
