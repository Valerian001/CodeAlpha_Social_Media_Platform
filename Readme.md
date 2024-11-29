# Social Media Platform

This is a simple social media platform built using **Django** that allows users to register, follow other users, and manage their profiles.

## Features

1. **User Registration and Authentication**  
   - New users can register for an account.  
   - Users can log in and log out securely.  

2. **User Profiles**  
   - Each user has a profile linked to their account.  
   - Profiles include a bio and the ability to follow/unfollow other users.

3. **Follow System**  
   - Users can follow and unfollow each other.  
   - Followers and following relationships are managed through a `ManyToManyField` in the `UserProfile` model.

4. **Homepage or Feed**  
   - Display posts or updates from the users a user follows.  

5. **Admin Dashboard**  
   - Admins can manage user accounts, profiles, and other aspects of the platform through Django's admin panel.

## Author
Developed by **Valerian**. For questions or suggestions, feel free to reach out.