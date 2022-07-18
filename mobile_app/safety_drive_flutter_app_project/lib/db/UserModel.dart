class UserModel {
  final String email;
  final String pseudo;
  final String password;
  final String uid;

  UserModel({
    required this.uid,
    required this.email,
    required this.pseudo,
    required this.password,
  });
}