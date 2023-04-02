package com.example.backendjava.service.function;

import org.htmlparser.Parser;
import org.htmlparser.beans.StringBean;
import org.htmlparser.filters.NodeClassFilter;
import org.htmlparser.tags.LinkTag;
import org.htmlparser.util.NodeList;
import org.htmlparser.util.ParserException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@Service
public class LinkExtractor {

//    private static String test_url = "https://cse.hkust.edu.hk/~dlee/4321/";

    public List<String> getAllLinks(String baseUrl) {
        ArrayList<String> returnList = new ArrayList<>();

        try {
            StringBean stringBean = new StringBean();
            stringBean.setURL(baseUrl);
            Parser parser = new Parser(baseUrl);
            NodeList list = parser.extractAllNodesThatMatch(new NodeClassFilter(LinkTag.class));

            for (int i = 0; i < list.size(); i++) {
                LinkTag link = (LinkTag) list.elementAt(i);
                String link_ = link.getLink();
                if (link_.substring(0, 4).equals("http")) {
                    returnList.add(link_);
                }
            }

        } catch (ParserException e) {
            e.printStackTrace();
        }

        return returnList;
    }


}
