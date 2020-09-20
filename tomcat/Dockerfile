FROM tomcat

RUN  rm -rf /usr/local/tomcat/webapps && \
  mv /usr/local/tomcat/webapps.dist /usr/local/tomcat/webapps

COPY  ./manager-context.xml /usr/local/tomcat/webapps/manager/META-INF/context.xml