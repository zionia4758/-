package web_Client;
import java.io.* ; 
import java.net.* ; 
import java.util.* ;

public class WebClient {

	public static void main(String[] args) throws IOException{
		WebClient client=new WebClient();  
		Scanner scan=new Scanner(System.in);
		String str="";
		String select="Post";
		String s="";
		String postData;
		while(!select.equals("Exit")) {
			System.out.print("Select type(Get,Post,JpgGet,AnswerToURL):");
			select=scan.nextLine();
			if(select.equals("Get")) {
				System.out.println("Get");

				System.out.print("URL:");
				str=scan.nextLine();
				s = client.getWebContentByGet(str);  
				System.out.println(s);
			}
			else if(select.equals("Post")) {

				System.out.println("Post");

				System.out.print("URL:");
				str=scan.nextLine();
				System.out.print("Data:");
				postData=scan.nextLine();
				s = client.getWebContentByPost(str,postData);  
				System.out.println(s);	
			}
			else if(select.equals("JpgGet")) {
				System.out.println("JpgGet");

				System.out.print("URL:");
				str=scan.nextLine();
				
				client.getImageContentByGet(str); 
			}
			else if(select.equals("AnswerToURL")) {
				System.out.println("Answer");
				str=str.replace("index.html","picResult");
				System.out.println("posturl: "+str);
				s=client.getWebContentByPost(str,"2016025196/"+client.imageCheck(s));
				System.out.println(s);
			}
		}
		//html받기
		
		//답안 제출
		
		
		//숫자 받기
		
		//이미지 다운로드
		
	}
	
	public void getIndexPage(String index) throws IOException {
		OutputStream output=new FileOutputStream("./index.html");
		byte[] by=index.getBytes();
		output.write(by);
		output.close();
	}
	public void getImagePage(String index) throws IOException {
		OutputStream output=new FileOutputStream("./image.jpg");
		byte[] by=index.getBytes();
		output.write(by);
		output.close();
	}
	public String imageCheck(String s) {

		StringTokenizer token=new  StringTokenizer(s,"\n");
		ArrayList<String> strarr=new ArrayList<String>();
		while(token.hasMoreTokens()) {
			String str=token.nextToken();
			//System.out.println(str);
			if(str.contains("index/images")) {
				//System.out.println(str);
				strarr.add(str);
			}
		}
		return Integer.toString(strarr.size());
	}
	public String getWebContentByPost(String urlString,String data) throws IOException {  
		return getWebContentByPost(urlString, data,"UTF-8", 5000);//iso-8859-1  
	}  

	public String getWebContentByGet(String urlString) throws IOException { 
		
		return getWebContentByGet(urlString, "iso-8859-1", 5000);  
	} 
	public String getImageContentByGet(String urlString) throws IOException{
		return getImageContentByGet(urlString,"UTF-8",5000);
	}
	public String getImageContentByGet(String urlString,final String charset,int timeout)throws IOException{
		if(urlString==null||urlString.length()==0) {
			return null;
		}
		urlString=(urlString.startsWith("http://")|| urlString.startsWith("https://"))
				?urlString : ("http://"+urlString).intern();
		URL url=new URL(urlString);
		HttpURLConnection conn=(HttpURLConnection) url.openConnection();
		conn.setRequestMethod("GET");
		conn.setRequestProperty("User-agent",
				"2016025196/KIMDONGKYU/WebClient/ComNet");
		
		conn.setRequestProperty("Accept","image/jpg");
		conn.setConnectTimeout(timeout);
		try {
			if(conn.getResponseCode() !=HttpURLConnection.HTTP_OK) {
				return null;
			}
		}catch(IOException e) {
			e.printStackTrace();
			return null;
		}
		InputStream input=conn.getInputStream();
		OutputStream file=new FileOutputStream("./image.jpg");
		try {
	         byte[] bytes = new byte[2048];
	         int length;

	         while ((length = input.read(bytes)) != -1) {
	        	 file.write(bytes, 0, length);
	         }
	       } finally {
	         input.close();
	         file.close();
	       }
		if(file!=null) {
			file.close();
		}
		if(conn!=null) {
			conn.disconnect();
		}
		return null;
		
	}
	public String getWebContentByGet(String urlString, final String charset, int timeout) throws IOException {
		if(urlString==null||urlString.length()==0) {
			return null;
		}
		urlString=(urlString.startsWith("http://")|| urlString.startsWith("https://"))
				?urlString : ("http://"+urlString).intern();
		URL url=new URL(urlString);
		HttpURLConnection conn=(HttpURLConnection) url.openConnection();
		conn.setRequestMethod("GET");
		conn.setRequestProperty("User-agent",
				"2016025196/KIMDONGKYU/WebClient/ComNet");
		
		conn.setRequestProperty("Accept","text/html");
		conn.setConnectTimeout(timeout);
		try {
			if(conn.getResponseCode() !=HttpURLConnection.HTTP_OK) {
				return null;
			}
		}catch(IOException e) {
			e.printStackTrace();
			return null;
		}
		InputStream input=conn.getInputStream();
		BufferedReader reader=new BufferedReader(new InputStreamReader(input,charset));
		String line=null;
		StringBuffer sb=new StringBuffer();
		while((line=reader.readLine())!=null) {
			sb.append(line).append("\r\n");
		}
		if(reader!=null) {
			reader.close();
		}
		if(conn!=null) {
			conn.disconnect();
		}
		return sb.toString();
		
	}

	public String getWebContentByPost(String urlString, String data, final String charset, int timeout) throws IOException{
	if(urlString==null||urlString.length()==0) {
		return null;
	}
	urlString=(urlString.startsWith("http://")||urlString.startsWith("https://"))
			? urlString :  ("http://"+urlString).intern();
	URL url=new URL(urlString);
	HttpURLConnection connection=(HttpURLConnection)url.openConnection();
	
	connection.setDoOutput(true);
	connection.setDoInput(true);
	connection.setRequestMethod("POST");
	
	connection.setUseCaches(false);
	connection.setInstanceFollowRedirects(true);
	
	connection.setRequestProperty("Content-Type","text/xml;charset=UTF-8");
	
	connection.setRequestProperty("User-Agent", "2016025196/KIMDONGKYU/WebClient/ComNet");
	
	connection.setRequestProperty("Accept", "text/xml");
	connection.setConnectTimeout(timeout);
	connection.connect();
	DataOutputStream out =new DataOutputStream(connection.getOutputStream());
	
	byte[] content=data.getBytes("UTF-8");
	
	out.write(content);
	out.flush();
	out.close();
	
	try {
		if(connection.getResponseCode()!=HttpURLConnection.HTTP_OK) {
			return null;
		}
	}catch(IOException e) {
		e.printStackTrace();
		return null;
	}
	BufferedReader reader= new BufferedReader(new InputStreamReader(connection.getInputStream(),charset));
	String line;
	StringBuffer sb=new StringBuffer();
	while((line=reader.readLine())!=null) {
		sb.append(line).append("\r\n");
	}
	if(reader!=null) {
		reader.close();
	}
	if(connection!=null) {
		connection.disconnect();
	}
	return sb.toString();
	} 
}
