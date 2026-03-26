#include <QDialog>
#include <QPushButton>
#include <QHBoxLayout>
#include <QDebug>

class MyDlg : public QDialog {
Q_OBJECT
private:
	QPushButton *pBttn1, *pBttn2, *pBttn3;
	QHBoxLayout *pLayout;
public:
	MyDlg();
	~MyDlg();
private slots:
	void onButton1Clicked();
	void onButton2Clicked();
	void onButton3Clicked();

};
