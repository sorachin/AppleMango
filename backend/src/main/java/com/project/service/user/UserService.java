package com.project.service.user;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Repository;
import org.springframework.stereotype.Service;

import javax.persistence.EntityManagerFactory;
import javax.persistence.PersistenceContext;
import javax.persistence.PersistenceUnit;
import javax.servlet.http.HttpSession;
import javax.transaction.Transactional;
import java.lang.Object;
import java.time.LocalDateTime;

import com.project.dao.user.UserDAO;
import com.project.model.user.Role;

import com.project.dao.user.*;

import com.project.model.user.UserEntity;

import io.swagger.annotations.ApiResponse;
import io.swagger.annotations.ApiResponses;
import io.swagger.annotations.ApiOperation;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;

import java.util.ArrayList;
import java.util.Enumeration;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Service
public class UserService implements UserDetailsService {

    @Autowired
    UserDAO userDAO;


    // @Autowired
    // SessionFactory sf;



    //회원가입
	public Object signUp(@RequestBody UserEntity request) {
        System.out.println(request);
        UserEntity newUser = new UserEntity();
        newUser.setUid(request.getUid());
        newUser.setUpw(request.getUpw());
        newUser.setUkind(request.getUkind());
        newUser.setUname(request.getUname());
        newUser.setUemail(request.getUemail());
        newUser.setUphone(request.getUphone());
        newUser.setUaddr(request.getUaddr());
        newUser.setUinstagramid(request.getUinstagramid());
        newUser.setUcreatedate(LocalDateTime.now());
        
        userDAO.save(newUser);
        
        return new ResponseEntity<UserEntity>(newUser, HttpStatus.OK);
	}
    


    //로그인
    public Object login(final String uid, final String upw, final HttpSession session) {

        final Optional<UserEntity> user = userDAO.findByUidAndUpw(uid, upw);

        ResponseEntity response = null;
        final ResponseBody result = new ResponseBody();

        if (user.isPresent()) {

            result.status = true;
            result.data = "success";

            user.ifPresent(u -> {
                System.out.println("email : " + u.getUemail());
                session.setAttribute("user", u);
                session.setAttribute("uid", u.getUid());
                session.setAttribute("upw", u.getUpw());
                session.setAttribute("uemail", u.getUemail());
                result.object = session.getAttribute("user");

            });
            response = new ResponseEntity<>(result, HttpStatus.OK);
        } else {
            response = new ResponseEntity<>("로그인 실패", HttpStatus.OK);
        }

        final Enumeration se = session.getAttributeNames();

        while (se.hasMoreElements()) {
            final String getse = se.nextElement() + "";
            System.out.println("@@@@@@@ session : " + getse + " : " + session.getAttribute(getse));
        }

        // session.setAttribute("user",user);

        // Session session = sf.getCurrentSession();
        // session.persist(user);

        System.out.println("리스판스" + result.object);
        return response;
    }

    public Object logout(final HttpSession session) {

        session.invalidate();

        return session;
    }


    @Override
    public UserDetails loadUserByUsername(String uid) throws UsernameNotFoundException {
        Optional<UserEntity> userEntityWrapper = userDAO.findByUid(uid);
        UserEntity userEntity = userEntityWrapper.get();

        List<GrantedAuthority> authorities = new ArrayList<>();

        if (("admin").equals(uid)) {
            authorities.add(new SimpleGrantedAuthority(Role.ADMIN.getValue()));
        } else {
            authorities.add(new SimpleGrantedAuthority(Role.MEMBER.getValue()));
        }

        return new User(userEntity.getUid(), userEntity.getUpw(), authorities);

    }
    
    //김연수추가
    public Object userInfo(String userId){
        
        UserEntity user = userDAO.getUserByUid(userId);

        return user;

    }






  
}


class ResponseBody {
    
    public boolean status = false;
    public String data;
    public Object object;
}
