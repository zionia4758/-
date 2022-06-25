package Webserver;
import java.io.*;
import java.net.*;
import java.util.*;

public class WebServer {

	public static void main(String[] args) throws IOException {
		ServerSocket S_sock= new ServerSocket(56616);
			
		try {
	
			while(true) {
				Socket sock=S_sock.accept();
				
				
				HttpRequest run_http_request=new HttpRequest(sock);
				Thread http_thread=new Thread(run_http_request);
				
				http_thread.start();
				
				
			}
			}
			catch (IOException e) {
				System.out.println(e.getMessage());
			}
			catch (Exception e) {
				System.out.println(e.getMessage());
			}
		S_sock.close();
	}	
	

}
