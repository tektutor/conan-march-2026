#include "MyDlg.h"

MyDlg::MyDlg() {
	qDebug() << "MyDlg constructor ...";

	pBttn1 = new QPushButton("Button 1");
	pBttn2 = new QPushButton("Button 2");
	pBttn3 = new QPushButton("Button 3");

	pLayout = new QHBoxLayout;

	pLayout->addWidget ( pBttn1 );
	pLayout->addWidget ( pBttn2 );
	pLayout->addWidget ( pBttn3 );

	setLayout( pLayout );

	connect (
		pBttn1,
		SIGNAL( clicked() ),
		this,
		SLOT ( onButton1Clicked() )
	);
	connect (
		pBttn2,
		SIGNAL( clicked() ),
		this,
		SLOT ( onButton2Clicked() )
	);
	connect (
		pBttn3,
		SIGNAL( clicked() ),
		this,
		SLOT ( onButton3Clicked() )
	);
}

MyDlg::~MyDlg() {
	qDebug() << "MyDlg destructor ...";

}

void MyDlg::onButton1Clicked() {
	qDebug() << "Button 1 Clicked";
}	

void MyDlg::onButton2Clicked() {
	qDebug() << "Button 2 Clicked";
}	

void MyDlg::onButton3Clicked() {
	qDebug() << "Button 3 Clicked";
}	

