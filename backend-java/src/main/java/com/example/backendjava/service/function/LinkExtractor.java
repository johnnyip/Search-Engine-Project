package com.example.backendjava.service.function;

import org.htmlparser.Parser;
import org.htmlparser.beans.StringBean;
import org.htmlparser.filters.NodeClassFilter;
import org.htmlparser.tags.LinkTag;
import org.htmlparser.util.NodeList;
import org.htmlparser.util.ParserException;
import org.springframework.stereotype.Service;

import java.io.IOException;
import java.net.MalformedURLException;
import java.net.URL;
import java.net.URLConnection;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;

@Service
public class LinkExtractor {

//    private static String test_url = "https://cse.hkust.edu.hk/~dlee/4321/";

    public List<String> getAllLinks(String baseUrl) {
        ArrayList<String> returnList = new ArrayList<>();

        try {
            URL url = new URL(baseUrl);
            URLConnection connection = url.openConnection();
            Date lastModifiedDate = new Date(connection.getLastModified());

            int contentLength = connection.getContentLength();

            StringBean stringBean = new StringBean();
            stringBean.setURL(baseUrl);
            Parser parser = new Parser(baseUrl);
            NodeList list = parser.extractAllNodesThatMatch(new NodeClassFilter(LinkTag.class));

            for (int i = 0; i < list.size(); i++) {
                LinkTag link = (LinkTag) list.elementAt(i);
                String link_ = link.getLink();
                if (link_.length() > 4 && link_.substring(0, 4).equals("http")) {
                    returnList.add(link_);
//                    returnList.add(link_+", "+lastModifiedDate);
                }
            }

        } catch (ParserException e) {
            e.printStackTrace();
        } catch (MalformedURLException e) {
            throw new RuntimeException(e);
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        return returnList;
    }


}
