package Webserver;
import java.io.*;
import java.net.*;
import java.util.*;

enum StatusCode{
	OK, BAD_REQUEST, FORBIDDEN, NOT_FOUND, HTTP_VERSION_NOT_SUPPORTED, INTERNAL_SERVER_ERROR
}


class HttpRequest implements Runnable{
	final static String CRLF="/r/n";
	final static String HTTP_VERSION = "1.1";
	final static String DEFAULT_CONTENT_TYPE="application/octet-stream";
	final static int BUFFER_IN_SIZE=2048;
	final static int BUFFER_OUT_SIZE = 2048;
	final static Properties CONTENT_TYPES=new Properties();
	final static EnumMap<StatusCode,String> SCODES =new EnumMap<StatusCode,String> (StatusCode.class);
	
	static {
		CONTENT_TYPES.setProperty("html","text/html");
		CONTENT_TYPES.setProperty("jpg", "image/jpeg");
		
		SCODES.put(StatusCode.OK,"200");
		SCODES.put(StatusCode.BAD_REQUEST,"400");
		SCODES.put(StatusCode.FORBIDDEN,"403");
		SCODES.put(StatusCode.NOT_FOUND, "404");
		
		SCODES.put(StatusCode.HTTP_VERSION_NOT_SUPPORTED, "505");
	}
	StatusCode code;
	Socket sock;
	File requestedFile;
	
	public HttpRequest(Socket sock) throws Exception{
		this.sock=sock;
		this.code=null;
		this.requestedFile=null;
	}
	
	public void run() {
		try {
			ProcessRequest();
			
			
			
			}catch(Exception e) {
				System.out.println("Exception occured while processing request: ");
				e.printStackTrace();
		}
	}
	
	private void ProcessRequest() throws Exception{
		InputStream is=null;
		DataOutputStream dos=null;
		FileInputStream fis=null;
		BufferedReader br=null;
		try {
			is=sock.getInputStream();
			dos=new DataOutputStream(sock.getOutputStream());
			br=new BufferedReader(new InputStreamReader(is),BUFFER_IN_SIZE);
			
			String requestLine=br.readLine();
			String errorMsg=parseRequestLine(requestLine);
			String headerLine=null;
			while((headerLine=br.readLine()).length()!=0) {
				System.out.println(headerLine);
			}
			if(errorMsg==null) {
				try {
					fis=new FileInputStream(requestedFile);
				}catch (FileNotFoundException e) {
					System.out.println("FileNotFoundException while opening file inputstream.");
					e.printStackTrace();
					code=StatusCode.NOT_FOUND;
				}
			}else {
				System.out.println();
				System.out.println(errorMsg);
			}
			sendResponseMessage(fis,dos);
			
			
		}finally {
			if(dos!=null)
				dos.close();
			if(br!=null)
				br.close();
			if(fis!=null)
				fis.close();
			sock.close();
		}
			
		
	}
	
	private static void sendBytes(FileInputStream fis,OutputStream dos) throws Exception{
		
		byte[] buffer = new byte[BUFFER_OUT_SIZE];
		int bytes=0;
		while((bytes=fis.read(buffer))!=-1) {
			dos.write(buffer,0,bytes);
		}
		System.out.println("send packet plz....");
	}
	
	private static String contentType(String file_name) {

		String fname=file_name.toLowerCase();
		int lastdot=fname.lastIndexOf(".");
		if((lastdot!= -1)&&(lastdot!=fname.length()-1)) {
			System.out.println("type : "+CONTENT_TYPES.getProperty(fname.substring(lastdot+1)));
			return CONTENT_TYPES.getProperty(fname.substring(lastdot+1),DEFAULT_CONTENT_TYPE);
			
		}
		return DEFAULT_CONTENT_TYPE;
	}
	
	private String parseRequestLine(String request_line) {
		System.out.println();
		System.out.println("Receuved HTTP request: ");
		System.out.println(request_line);
		StringTokenizer tokens =new StringTokenizer(request_line);
		
			
		if(tokens.countTokens()!=3) {
			code=StatusCode.BAD_REQUEST;
			return "Request line is malformed. Returning BAD Not Found.";
		}
		String method=tokens.nextToken().toUpperCase();
		String fileName=tokens.nextToken();
		fileName="."+fileName;
		System.out.println("File:"+fileName);
		File file=new File(fileName);
		
		if(!file.exists()) {
			code =StatusCode.NOT_FOUND;
			return "Requested file"+fileName + " does not exist. " + "Returning NOT FOUND.";
		}
		if(!file.canRead()) {
			code=StatusCode.FORBIDDEN;
			return "Requested file"+fileName + " is not readable. " + "Returning with FORBIDDEN.";
		}
		if(file.isDirectory()) {
			File[] list=file.listFiles(new FilenameFilter() {
				public boolean accept(File dir,String f) {
					if(f.equalsIgnoreCase("index.html"))
						return true;
					return false;
				}
			});
			if(list==null || list.length==0) {
				code = StatusCode.NOT_FOUND;
				return "No index file found at requsted location " + fileName
						+" Returning NOT FOUND";
			}
			else if(list.length==-1) {
				code = StatusCode.INTERNAL_SERVER_ERROR;
				return "Found more than one index file at requested location " + fileName
						+". Returning INTERNAL SERVER ERROR.";
			}
			file=list[0];
		}
		requestedFile=file;
		String version=tokens.nextToken().toUpperCase();
		System.out.println(version);
		if(version.equals("HTTP/1.0")) {
			code=StatusCode.HTTP_VERSION_NOT_SUPPORTED;
			return "HTTP version string is malformed. Returning BAD REQUEST.";
		}
		if(version.equals("HTTP/1.1")) {
			code = StatusCode.OK;
		return null;
		}
		if(!version.matches("HTTP/([1-9][0-9.]]*)")) {
			code = StatusCode.BAD_REQUEST;
			return "HTTP version string is malformed. Returning BAD REQUEST.";
		}
		if(!version.equals("HTTP/1.0")&& !version.equals("HTTP/1.1")) {
			code = StatusCode.HTTP_VERSION_NOT_SUPPORTED;
			return version + " not suppotrd. Returning HTTP VERSION NOT SUPPORTED.";
		}
		code = StatusCode.OK;
		return null;
	}
	private void sendResponseMessage(FileInputStream fis,DataOutputStream dos) throws Exception{
		String statusLine = "HTTP/"+HTTP_VERSION+" " +SCODES.get(code)+" ";
		String entityBody="<HTML>"+CRLF+" <HEAD><TITLE>sent by dongkyu's Webserver</TITLE></HEAD>"+CRLF+" <BODY>?</BODY>"+CRLF
				+"</HTML>";
		String message;
		switch(code) {
		case OK:
			message="OK";
			break;
		case BAD_REQUEST:
			message="Bad Request";
			break;
		case FORBIDDEN:
			message="Forbidden";
			break;
		case NOT_FOUND:
			message="Not Found";
			break;
		case HTTP_VERSION_NOT_SUPPORTED:
			message="HTTP Version Not Supported";
			break;
		default:
			message = "What is this???";
		}
		statusLine=statusLine+ message;
		System.out.println(code.toString());
		
		System.out.println("statusLine: "+statusLine);
		System.out.println("entityBody:"+CRLF+entityBody);
		dos.writeBytes(statusLine + CRLF);
		sendHeaderLines(dos);
		dos.writeBytes(CRLF);
		
		if(code==StatusCode.OK) {
			System.out.println("Sending requested file to client...");
			sendBytes(fis,dos);
		}
		else {
			System.out.println("Sending error message to client...");
			dos.writeBytes(entityBody);
		}
		
	}
	private void sendHeaderLines(DataOutputStream dos)throws Exception{
		StringBuffer headerLines = new StringBuffer();
		
		String contentTypeLine="Content-Type: ";
		String contentLength = "Content-Length: ";
		System.out.println("code "+code);
		switch(code) {
		case OK:
			contentTypeLine+=contentType(requestedFile.getName())+CRLF;
			contentTypeLine+=contentLength + requestedFile.length() + CRLF;
			break;
		default:
			contentTypeLine+="text/html "+CRLF;
			}
		headerLines.append(contentTypeLine);
		dos.writeBytes(headerLines.toString());
	}
	
}
