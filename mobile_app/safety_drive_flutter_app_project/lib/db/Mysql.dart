import 'package:mysql1/mysql1.dart';


class Mysql {
  static String host = 'aurora-instance-safety-drive.cjp8zgshnmam.us-east-1.rds.amazonaws.com',
      user = 'safetyDriveAdmin',
      password = 'safety-drive',
      db = 'safety_drive_db';
  static int port = 3306; 

  Future<MySqlConnection> getConnection() async {
    var settings = ConnectionSettings(
        host: host, 
        port: port, 
        user: user, 
        password: password, 
        db: db,
        );
    return await MySqlConnection.connect(settings);
  }
}