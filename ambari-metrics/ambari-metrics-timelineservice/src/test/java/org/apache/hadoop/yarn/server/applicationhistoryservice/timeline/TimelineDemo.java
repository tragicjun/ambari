package org.apache.hadoop.yarn.server.applicationhistoryservice.timeline;

import com.google.gson.Gson;
import org.apache.hadoop.yarn.api.records.timeline.TimelineEntities;
import org.apache.hadoop.yarn.api.records.timeline.TimelineEntity;
import org.apache.hadoop.yarn.api.records.timeline.TimelineEvent;

/**
 * Created by jerryjzhang on 2016/1/23.
 */
public class TimelineDemo {
    static Gson gson = new Gson();

    public static void main(String []  args){
        TimelineEntities entities = new TimelineEntities();

        TimelineEntity entity = new TimelineEntity();
        entity.setEntityType("SYSTEM_AUDIT");
        entity.setEntityId("123");
        entity.setStartTime(System.currentTimeMillis());
        TimelineEvent event = new TimelineEvent();
        event.setEventType("SCHEDULE_TASK");
        event.setTimestamp(System.currentTimeMillis());
        event.addEventInfo("user","admin");
        event.addEventInfo("service","lhotse");
        entity.getEvents().add(event);
        entity.addPrimaryFilter("user","admin");
        entity.addPrimaryFilter("service","lhotse");
        entities.addEntity(entity);

        entity = new TimelineEntity();
        entity.setEntityType("SYSTEM_AUDIT");
        entity.setEntityId("1234");
        entity.setStartTime(System.currentTimeMillis());
        event = new TimelineEvent();
        event.setEventType("START_WORKFLOW");
        event.setTimestamp(System.currentTimeMillis());
        event.addEventInfo("user","admin");
        event.addEventInfo("service","nifi");
        entity.getEvents().add(event);
        entity.addPrimaryFilter("user","admin");
        entity.addPrimaryFilter("service","nifi");
        entities.addEntity(entity);

        entity = new TimelineEntity();
        entity.setEntityType("LHOTSE");
        entity.setEntityId("20150602142023792");
        entity.setStartTime(System.currentTimeMillis());
        event = new TimelineEvent();
        event.setEventType("FAILED");
        event.setTimestamp(System.currentTimeMillis());
        event.addEventInfo("user","admin");
        event.addEventInfo("service","nifi");
        entity.getEvents().add(event);
        entity.addPrimaryFilter("user","admin");
        entity.addPrimaryFilter("service","nifi");
        entities.addEntity(entity);

        System.out.println(gson.toJson(entities));
    }
}
