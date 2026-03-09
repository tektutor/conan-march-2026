#include <iostream>
#include <mysql_driver.h>
#include <mysql_connection.h>
#include <cppconn/statement.h>
#include <cppconn/resultset.h>

int main() {
	try {
		sql::mysql::MySQL_Driver *pDriver;
		sql::Connection *pConnection;

		pDriver = sql::mysql::get_mysql_driver_instance();
		pConnection = pDriver->connect("tcp://127.0.0.1:3306", "root", "root@123");

		pConnection->setSchema("tektutor");

		sql::Statement *pStatement;
		sql::ResultSet *pResultSet;

		pStatement = pConnection->createStatement();
		pResultSet = pStatement->executeQuery( "SELECT id, name FROM users");

		while ( pResultSet->next() ) {
			std::cout << "ID: " << pResultSet->getInt("id")
			          << "Name : " << pResultSet->getString("name")
				  << std::endl;
		}

		delete pResultSet;
		delete pStatement;
		delete pConnection;
	}
	catch (exception e) {
		std::cout << "Unable to connect to mysql server" << std::endl;
		return 1;
	}

	return 0;
}
