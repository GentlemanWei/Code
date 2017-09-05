# include <iostream>
# include <string>
# include <stdio.h>

using namespace std;

int main ()
{
	string number[10]={"ling","yi","er","san","si","wu","liu","qi","ba","jiu"};
	char a[101];
	int sum=0,i=0;
	cin>>a;
	while(a[i]!='\0'){
		sum+=a[i]-'0';
		++i;
	}
	int b[11],j=0;
	if(sum==0){
		cout << number[0];
		return 0;
	}
	while(sum!=0){
		b[j]=sum%10;
		sum=sum/10;
		++j;
	}
	for(int i=j-1;i>0;--i){
		cout << number[b[i]];
		cout<<" ";
	}
	cout << number[b[0]];
	return 0;
} 
