#include <fstream>
#include <iostream>
#include "person.pb.h"

using namespace std;

int main(int argc, char *argv[])
{
    Person personA;
    personA.set_name("Kil-Dong Hong");
    personA.set_email("kdhong@email.com");

#if 0
    //write textual string
    cout << personA.DebugString();
#endif

    //write binary
    fstream output("myfile.protobin", ios::out | ios::binary);
    personA.SerializeToOstream(&output);
    output.close();

    Person personB;
    //read binary
    fstream input("myfile.protobin", ios::in | ios::binary);
    personB.ParseFromIstream(&input);
    cout << "Name: " << personB.name() << endl;
    cout << "E-mail: " << personB.email() << endl;
    input.close();
    
    return 0;
}
