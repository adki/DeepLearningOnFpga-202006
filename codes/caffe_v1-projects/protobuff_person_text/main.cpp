#include <fstream>
#include <iostream>
#include <fcntl.h>
#include <unistd.h>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/io/zero_copy_stream_impl.h>
#include <google/protobuf/text_format.h>
#include "person.pb.h"

using namespace std;
using google::protobuf::io::FileInputStream;
using google::protobuf::io::FileOutputStream;
using google::protobuf::io::ZeroCopyInputStream;
using google::protobuf::io::CodedInputStream;
using google::protobuf::io::ZeroCopyOutputStream;
using google::protobuf::io::CodedOutputStream;

int main(int argc, char *argv[])
{
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    Person personA;
    personA.set_name("Kil-Dong Hong");
    personA.set_email("kdhong@email.com");

#if 0
    //write textual string
    cout << person.DebugString();
#endif

#if 0
    //write textual file
    int fdA = open("myfile.prototxt", O_WRONLY | O_CREAT | O_TRUNC, 0644);
    FileOutputStream *output = new FileOutputStream(fdA);
    google::protobuf::TextFormat::Print(personA, output);
    delete output;
    close(fdA);
#endif
    
    Person personB;
    //read textual file
    int fdB = open("myfile.prototxt", O_RDONLY);
    FileInputStream *input = new FileInputStream(fdB);
    google::protobuf::TextFormat::Parse(input, &personB);
    delete input;
    close(fdB);
    cout << "Name: " << personB.name() << endl;
    cout << "E-mail: " << personB.email() << endl;
    
    return 0;
}
